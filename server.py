import socket
import sys
import os

if not os.path.exists("data/"):
    os.mkdir("data/")

USAGE = "Usage: python server.py [host] [port]"
LOG_PATH = "data/logs.txt"

def throw_usage_error(message):
    print(message)
    print(USAGE)
    sys.exit(1)

def check_args_length():
    if len(sys.argv) < 3:
        throw_usage_error("Not enough arguments.")
    if len(sys.argv) > 3:
        throw_usage_error("Too many arguments.")

def validate_args(host, port):
    host_split = host.split('.')
    if not (len(host_split) == 4 and min([(o.isnumeric() and int(o) >= 0 and int(o) < 0xff) for o in host_split]) == 1):
        throw_usage_error("Not a valid IP.")
    if not (port.isnumeric() and int(port) >= 0 and int(port) < 0xffff):
        throw_usage_error("Not a valid port.")

def open_socket(host, port):
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    return s

def send_response(connection, webpage_path, content_type):
    with open(webpage_path, "r") as page:
        page_str = page.read()
        header = f"HTTP/1.0 200 OK\r\nContent-Type: {content_type}; charset=utf-8\r\nConnection: close\r\n"
        http_message = header + "\r\n" + page_str
        connection.send(http_message.encode("utf-8"))
        print("sent response")

def parse_data(data):
    data_split = data.split('\r\n\r\n')
    start_headers_split = data_split[0].split('\r\n')
    start_split = start_headers_split[0].split()
    headers = start_headers_split[1:]
    body = data_split[1] if len(data_split) > 1 else ""

    method = start_split[0].upper()
    uri = start_split[1].split("?")
    path = uri[0]

    query_parameters_dict = {}
    if len(uri) > 1:
        query_parameters_split = uri[1].split("&")
        query_parameters_dict = {k:v for k, v in (q.split("=") for q in query_parameters_split)}

    return method, path, headers, query_parameters_dict, body

def log_post(payload, file_path):
    with open(file_path, "a") as f:
        f.write(payload + '\n')

def server_run(host, port):
    s = open_socket(host, port)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by ', addr)
            data = conn.recv(1024).decode("utf-8")
            print(data)

            method, path, headers, query_parameters, request_body = parse_data(data)
            print("Parsed request:")
            print(method)
            print(path)
            print(headers)
            print(query_parameters)
            print(request_body)

            if method == "GET":
                if path == "/":
                    send_response(conn, "page/index.html", "text/html")
                elif path == "/css/style.css":
                    send_response(conn, "page/css/style.css", "text/css")
            elif method == "POST":
                if path == "/submit":
                    log_post(request_body, LOG_PATH)
                    send_response(conn, "page/success.html", "text/html")
            
            conn.close()

if __name__ == "__main__":
    check_args_length()
    host, port = sys.argv[1], sys.argv[2]
    validate_args(host, port)
    server_run(host, port)
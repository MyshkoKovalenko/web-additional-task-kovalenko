import socket
import sys

HOST = None
PORT = 33333

HEADERS = "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n"

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
    

def send_response(connection):
    with open("page/index.html", "r") as page:
        page_str = page.read()
        http_message = HEADERS + f"Content-length: {len(page_str)}\r\n" + "\r\n" + page_str
        connection.send(http_message.encode("utf-8"))
        print("sent")

def server_run():
    s = open_socket(HOST, PORT)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            send_response(conn)
            conn.close()

if __name__ == "__main__":
    server_run()
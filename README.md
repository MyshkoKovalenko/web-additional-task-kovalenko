# Simple HTTP Server

A simple HTTP server that can respond to GET and POST requests and also parse query parameters.

## How to run?
```
python server.py [host] [port]
```

## How to use?

Go to `http://<host>:<port>` in a web browser (e. g. `http://127.0.0.1:8080`).

There will be a form with 2 fields, which are username and message, that a user can fill out and submit. The server will receive a POST request and log the response to a `data/logs.txt` file.

There is also a link to another page with another form. Here, a user can write a username and search for all messages attributed to that username. The search is implemented using the query parameters.
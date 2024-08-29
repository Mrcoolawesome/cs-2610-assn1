import socket
from router_middleware import middleware_router
from http_parser import request_parser
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8080))
    s.listen()
    print("listening on port 8000")

    while True:
        connection, addr = s.accept()
        with connection:
            data = connection.recv(8192)
            if not data:
                connection.close()
                continue

            http_request = request_parser(data)
            data = middleware_router(http_request)
            connection.send(data)

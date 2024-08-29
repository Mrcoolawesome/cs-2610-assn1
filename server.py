import socket
from router_middleware import middleware_router
from http_parser import request_parser
from http_encoder import encoder

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8000))
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
            response_object = middleware_router(http_request)
            encoded_response = encoder(response_object)
            connection.send(encoded_response)

import socket
from router_middleware import middleware_router
from http_parser import request_decoder
from http_encoder import encoder

# main loop that's responsible for sending and receiving data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    port = 8000
    s.bind(("127.0.0.1", port))
    s.listen()
    print(f"listening on port {port}")

    while True:
        connection, addr = s.accept()
        with connection:
            data = connection.recv(8192)
            if not data:
                connection.close()
                continue

            # creates an http_request object, then get's a response object based off of that request
            http_request = request_decoder(data)
            response_object = middleware_router(http_request)
            
            # then that response is encoded into bytes, then sent to the client
            encoded_response = encoder(response_object)
            connection.send(encoded_response)

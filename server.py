import socket, http_parser

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

            print(http_parser.request_parser(data))
            #TODO: parse the request, send through middleware and encode the response
            
            connection.send(bytes(res, "UTF-8"))
            
def send_bytes(bytes):
    connection, addr = s.accept()
    connection.send(bytes)
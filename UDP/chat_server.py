import socket

HOST = '127.0.0.1'
PORT = 23457
BUFFER_SIZE = 4096

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"UDP Chat Server listening on {HOST}:{PORT} ...")

client_address = None

try:
    while True:
        # Receive from client
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        message = data.decode().strip()

        if client_address is None:
            client_address = addr
            print(f"Client connected from {client_address}")

        print(f"Client: {message}")

        if message.lower() == 'exit':
            server_socket.sendto("Goodbye! Closing session.".encode(), addr)
            break

        # Server types a reply
        server_message = input("You (server): ")
        server_socket.sendto(server_message.encode(), addr)

        if server_message.lower() == 'exit':
            break
finally:
    server_socket.close()
    print("Server closed.")

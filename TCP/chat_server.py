import socket

HOST = '127.0.0.1'
PORT = 23456
BUFFER_SIZE = 4096

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"TCP Chat Server listening on {HOST}:{PORT} ...")

conn, addr = server_socket.accept()
print(f"Client connected from {addr}")

try:
    while True:
        # Receive from client
        data = conn.recv(BUFFER_SIZE)
        if not data:
            print("Client disconnected")
            break
        message = data.decode().strip()
        print(f"Client: {message}")

        if message.lower() == 'exit':
            conn.sendall("Goodbye! Closing connection.".encode())
            break

        # Server types a reply
        server_message = input("You (server): ")
        conn.sendall(server_message.encode())

        if server_message.lower() == 'exit':
            break
finally:
    conn.close()
    server_socket.close()
    print("Server closed.")

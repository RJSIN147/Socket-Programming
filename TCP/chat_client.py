import socket

HOST = '127.0.0.1'
PORT = 23456
BUFFER_SIZE = 4096

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to TCP Chat Server at {HOST}:{PORT}")


try:
    while True:
        message = input("You (client): ")
        client_socket.sendall(message.encode())

        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            print("Server closed the connection.")
            break
        print("Server:", data.decode().strip())

        if message.lower() == 'exit':
            break
finally:
    client_socket.close()
    print("Client closed.")

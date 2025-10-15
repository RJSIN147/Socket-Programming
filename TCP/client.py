import socket

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect(('127.0.0.1', 12345))

# Send data
client_socket.sendall("Hello from client!".encode())

# Receive response
data = client_socket.recv(1024).decode()
print("Server says:", data)

# Close
client_socket.close()

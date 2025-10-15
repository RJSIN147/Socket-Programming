import socket

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to host and port
server_socket.bind(('127.0.0.1', 12345))

# Start listening
server_socket.listen(1)
print("Server listening on port 12345...")

# Accept client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Receive data
data = conn.recv(1024).decode()
print("Client says:", data)

# Send response
conn.sendall("Hello from server!".encode())

# Close
conn.close()
server_socket.close()
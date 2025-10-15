import socket

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to host and port
server_socket.bind(('127.0.0.1', 12345))
print("Server listening on port 12345...")

# Receive data from client
data, client_address = server_socket.recvfrom(1024)
print("Client says:", data.decode())

# Send response to client
server_socket.sendto("Hello from server!".encode(), client_address)

# Close socket
server_socket.close()

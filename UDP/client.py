import socket

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
server_address = ('127.0.0.1', 12345)

# Send data to server
client_socket.sendto("Hello from client!".encode(), server_address)

# Receive response from server
data, _ = client_socket.recvfrom(1024)
print("Server says:", data.decode())

# Close socket
client_socket.close()

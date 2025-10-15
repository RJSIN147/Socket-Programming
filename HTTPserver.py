import socket

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow reuse of address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to localhost on port 8080
server_socket.bind(("127.0.0.1", 8080))
server_socket.listen(5)

print("HTTP Server running on http://127.0.0.1:8080")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive request
    request = client_socket.recv(1024).decode()
    print("----- HTTP REQUEST -----")
    print(request)
    print("------------------------")

    # Simple HTTP response
    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head><title>Mini Server</title></head>
<body>
<h1>Hello!</h1>
</body>
</html>
"""
    client_socket.sendall(response.encode())
    client_socket.close()

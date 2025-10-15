import socket
import threading

# Server configuration
HOST = "127.0.0.1"
PORT = 8080

# HTTP response template
RESPONSE = """\
HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<html>
<head><title>Mini Server</title></head>
<body>
<h1>Hello from Python Mini HTTP Server</h1>
<p>This is a threaded, raw socket HTTP response!</p>
</body>
</html>
"""

# Function to handle each client
def handle_client(client_socket, addr):
    try:
        request = client_socket.recv(1024).decode()
        print(f"----- HTTP REQUEST from {addr} -----")
        print(request)
        print("-----------------------------------")

        client_socket.sendall(RESPONSE.encode())
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        client_socket.close()

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Threaded HTTP Server running on http://{HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
except KeyboardInterrupt:
    print("\nServer is shutting down...")
finally:
    server_socket.close()

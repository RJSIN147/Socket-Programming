# Client-Server Networking Examples (TCP, UDP, and Minimal HTTP)

This repository contains simple Python examples that demonstrate the client-server model using TCP, UDP, and a minimal HTTP server. The goal is to help beginners who have never done socket programming understand how data flows between a client and a server over a network.

### What is the Client-Server Model?
- **Client**: An application that initiates a request. It asks for something (like data or a web page).
- **Server**: An application that listens for requests and responds. It provides the requested service or data.
- **Request/Response**: The client sends a request; the server processes it and sends back a response.
- **Address and Port**: To find each other, the client needs the server's IP address and port number. In these examples, we use `127.0.0.1` (localhost) which means "this computer," so no internet is required.
- **Protocols**: Rules for communication. Here we use:
  - **TCP (Transmission Control Protocol)**: Reliable, connection-based (ensures data arrives in order, resends lost data).
  - **UDP (User Datagram Protocol)**: Unreliable, connectionless (faster, but no guarantee of delivery or order).
  - **HTTP (HyperText Transfer Protocol)**: An application-layer protocol commonly used for the web (built on top of TCP).

Beginner tip: Always start the server first (so it is listening) and then run the client that connects to it.

---

## TCP examples (reliable, connection-oriented)

What makes TCP special for beginners:
- It creates a virtual "connection" between client and server (a reliable pipe).
- Packets are resent if lost, and data arrives in order.
- You read and write a byte stream, not message-sized chunks.

### `TCP/server.py` — Basic TCP server (single client example)

```1:26:d:\CN\TCP\server.py
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
```
- `AF_INET`: IPv4 addressing (four numbers like 127.0.0.1). For IPv6 you’d use `AF_INET6`.
- `SOCK_STREAM`: TCP stream-oriented sockets (a continuous flow of bytes).
- `bind(('127.0.0.1', 12345))`: Makes the OS route incoming traffic on port 12345 (localhost) to this socket.
- `listen(1)`: Enables incoming connections; `1` is backlog (pending-connection queue length), not "only one client ever".
- `accept()`: Blocks until a client connects; returns a new socket just for that client, leaving `server_socket` to keep listening.
- `recv(1024)`: Reads up to 1024 bytes. If the message were larger, TCP could split it; you might need a loop in real apps.
- `sendall(...)`: Sends all bytes (retries internally). Always send bytes, so we use `.encode()` on strings.
- `close()`: Cleanly releases resources.

How to run (PowerShell):
- Start the server: `python .\\TCP\\server.py`

### `TCP/client.py` — Basic TCP client

```1:18:d:\CN\TCP\client.py
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
```
- `connect(...)`: Initiates the TCP handshake (SYN, SYN-ACK, ACK) under the hood.
- `sendall(...)` then `recv(...)`: Typical request/response pattern.
- Errors you might see:
  - `ConnectionRefusedError`: Server not running or wrong port.
  - Hanging on `recv`: Server didn’t send anything yet; blocking calls wait.

How to run (PowerShell):
- With the server running, start the client: `python .\\TCP\\client.py`

---

## UDP examples (faster, connectionless)

What makes UDP different:
- No connection or handshake; you just send datagrams to an address.
- Faster, but delivery and order are not guaranteed.
- You read/write whole messages (datagrams), not a continuous stream.

### `UDP/server.py` — Basic UDP server

```1:19:d:\CN\UDP\server.py
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
```
- `SOCK_DGRAM`: UDP datagram sockets; each call to `recvfrom` returns one datagram.
- `recvfrom(1024)`: Also returns the sender’s address, since there’s no persistent connection.
- `sendto(...)`: You must specify the destination address each time.

How to run (PowerShell):
- Start the UDP server: `python .\\UDP\\server.py`

### `UDP/client.py` — Basic UDP client

```1:18:d:\CN\UDP\client.py
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
```
- Send a datagram using `sendto`, then wait for one with `recvfrom`.
- If nothing arrives, `recvfrom` blocks. Real apps might use timeouts with `settimeout(seconds)`.

How to run (PowerShell):
- With the UDP server running, run: `python .\\UDP\\client.py`

---

## Minimal HTTP over TCP (raw sockets)

HTTP is a text-based protocol built on top of TCP. Browsers send an HTTP request (like `GET / HTTP/1.1` with headers), and servers reply with a status line, headers, a blank line, and an optional body.

### `HTTPserver.py` — Minimal single-threaded HTTP server

```1:39:d:\CN\HTTPserver.py
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
```
- TCP under the hood: your browser connects via TCP to `127.0.0.1:8080`.
- `SO_REUSEADDR`: Avoids "address already in use" after restarts.
- HTTP response structure:
  - Status line: e.g., `HTTP/1.1 200 OK`.
  - Headers: metadata like `Content-Type: text/html`.
  - Blank line: must be present between headers and body.
  - Body: the HTML page content.
- The printed request shows method (`GET`), path (`/`), and headers.

How to run (PowerShell):
- Start: `python .\\HTTPserver.py`, then open `http://127.0.0.1:8080` in a browser.

### `MThttpserver.py` — Threaded minimal HTTP server (handles multiple clients)

```1:54:d:\CN\MThttpserver.py
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
```
- `threading` allows handling many clients simultaneously.
- `daemon=True`: Threads won’t block program exit; they stop when the main thread stops.
- Each connection is processed independently in `handle_client`, while the main loop immediately returns to `accept()`.
- `Connection: close` header indicates the server will close the TCP connection after the response.

How to run (PowerShell):
- Start: `python .\\MThttpserver.py`, then open multiple tabs to `http://127.0.0.1:8080`.

---

## Extra beginner notes and troubleshooting
- If you see "address already in use": another process is using the port. Either stop it or change the port number.
- Firewalls/antivirus can block local ports. Allow Python or try a different port.
- `accept()`, `recv()`, and `recvfrom()` are blocking; your program waits there until something happens. Use threads or non-blocking sockets for interactive apps.
- Network data is bytes. Use `.encode()` to send strings and `.decode()` to read them.
- `127.0.0.1` means your own machine. To communicate across machines, replace with the server’s IP and ensure they can reach each other over the network.
- On Windows PowerShell, run commands exactly as shown above; they assume your working directory is the repo root.
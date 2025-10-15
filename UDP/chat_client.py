import socket

HOST = '127.0.0.1'
PORT = 23457
BUFFER_SIZE = 4096

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (HOST, PORT)
print(f"Connected (UDP) to {HOST}:{PORT}. Type messages; 'exit' to quit.")


try:
    while True:
        message = input("You (client): ")
        client_socket.sendto(message.encode(), server_address)

        data, _ = client_socket.recvfrom(BUFFER_SIZE)
        print("Server:", data.decode().strip())

        if message.lower() == 'exit':
            break
finally:
    client_socket.close()
    print("Client closed.")

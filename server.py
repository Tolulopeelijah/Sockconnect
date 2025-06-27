messages = ['']
import socket
import threading

# Function to handle client connection
def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[{address}] {message}")
            client_socket.send("Message received".encode())
        except:
            break

    print(f"[DISCONNECTED] {address} disconnected.")
    client_socket.close()

# Main server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)

print("[STARTED] Server is listening on port 12345")

while True:
    client_socket, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

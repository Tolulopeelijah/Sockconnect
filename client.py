import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8000))

while True:
    message = input("You: ")
    if message.lower() == "exit":
        break
    client.send(message.encode())
    response = client.recv(1024).decode()
    print("Server:", response)

client.close()

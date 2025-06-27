# import socket

# # Create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to server
# client_socket.connect(('localhost', 12345))
# while True:
#     message = input()
#     # Send a message
#     client_socket.send(message.encode())
#     print('You: ', message)
#     # Receive response
#     response = client_socket.recv(1024).decode()
#     print(f"Server: {response}")

#     # Close connection
#     client_socket.close()



import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

while True:
    message = input("You: ")
    if message.lower() == "exit":
        break
    client.send(message.encode())
    response = client.recv(1024).decode()
    print("Server:", response)

client.close()

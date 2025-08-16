import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8000))
print('Welcome to the TICTACTOE Game')

for i in range(9):
    response = client.recv(1024).decode()
    if response == "your turn": 
        while True:
            message = input("Please make your move(exit to cancel): ")
            if message.lower() == "exit":
                break
            client.send(message.encode())
            if client.recv(1024).decode() == 'valid move':
                break
            else: print('Invalid move!')



client.close()

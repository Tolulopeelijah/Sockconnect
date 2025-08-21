import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8000))
print('Welcome to the TICTACTOE Game')

message = None
for i in range(9):
    if message in ['won', 'lost', 'draw']:
        break
    response = client.recv(1024).decode() # signal to know it's your turn
    if response == "your turn": 
        while True:
            move = input("Please make your move(exit to cancel): ")
            if move.lower() == "exit":
                break
            client.send(move.encode())
            message = client.recv(1024).decode() # valid or invalid move feedback
            if message == 'valid move':
                break
            elif message == 'won':
                print('yipee, you won')
                break
            elif message == 'lost':
                print("sorry, this didn't come your way")
                break
            elif message == 'draw':
                print('the game is a tie!')
                break
            else: 
                print(message)
                print('Invalid move!')



client.close()

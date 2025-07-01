import socket
import threading
import game_logic as game

logging = True
board = game.board
client_m = ['X',
            'O',
            'Resign',
            'Draw',
            ] # client's possible messages
server_m = ['Connection established',
            'Player 1/2 plays X/O',
            'Player 1/2 Resigned',
            'Invalid move',
            'Player 1/2 won',
            "It's a tie"]




def handle_client(client_socket, address, player = {}):
    player[address] = 'X' if player else 'O'
    print(f"Player {len(player)} connected")
    if logging and len(player) == 2:
        game.display(board)
    while True:
        move = client_socket.recv(1024).decode()
        if game.validate(board, move):
            game.update(board, move, player[address])
            break
        else:
            client_socket.send("The move has been occupied".encode())


    print(f"Player {player[address]} disconnected")

    client_socket.close()









server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8000))
server.listen(1)

if logging: print("Waiting for users to connect")

for i in range(2):
    client_socket, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()

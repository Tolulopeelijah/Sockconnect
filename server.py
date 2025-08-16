import socket
import game_logic as game
import threading


def winning_info():
    if game.check_win(board) == 'X':
        players[0][0].send("You won!".encode())
        game.display(board)
        
    elif game.check_win(board) == 'O':
        players[1][0].send("You won!".encode())
        game.display(board)
    elif game.check_win(board) == 'draw':
        for p in players:
            p[0].send("The game is a tie!".encode())
    

logging = True
board = game.board



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8000))
server.listen(1)

players = [server.accept() for _ in range(2)]
symbols = ['X', 'O']

def game_loop(client, sym):
    client.send("your turn".encode())
    while True:
        player = client.recv(1024).decode()
        if game.validate(board, player):
            client.send("valid move".encode())
            break
        else: player = client.send("Invalid move".encode())

    game.update(board, player, sym)
    game.display(board)
    winning_info()

for i in range(9):
    for i in range(2):
        thread = threading.Thread(target=game_loop, args=(players[i][0], symbols[i]))
        thread.start()























# def handle_client(client_socket, address, player = {}):
#     player[address] = 'X' if player else 'O'
#     print(f"Player {len(player)} connected")
#     if logging and len(player) == 2:
#         game.display(board)
#     while True:
#         move = client_socket.recv(1024).decode()
#         if game.validate(board, move):
#             game.update(board, move, player[address])
#             break
#         else:
#             client_socket.send("The move has been occupied".encode())


#     print(f"Player {player[address]} disconnected")

#     client_socket.close()











# if logging: print("Waiting for users to connect")

# for i in range(2):
#     client_socket, addr = server.accept()
#     thread = threading.Thread(target=handle_client, args=(client_socket, addr))
#     thread.start()

import socket
import game_logic as game
import threading

def handle_server():
    cmd = input()
    if input() == 'exit':
        print('exiting')
        server.close()

threading.Thread(target = handle_server, daemon = True).start()

def winning_info():
    result = game.check_win(board)
    if result == 'X':
        print(f"{game.check_win(board)} won")
        players[0][0].send("won".encode())
        players[1][0].send("lost".encode())
        return 'over'
        
    elif result == 'O':
        players[0][0].send("lost".encode())
        players[1][0].send("won".encode())
        return 'over'

    elif result == 'draw':
        for p in players:
            p[0].send("The game is a tie!".encode())
            return 'over'
    

logging = True
board = game.board



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8000))
server.listen(2)

players = [server.accept() for _ in range(2)]
symbols = ['X', 'O']

def game_loop(client, sym):
    client.send("your turn".encode())
    while True:
        player = client.recv(1024).decode()
        if game.validate(board, player):
            game.update(board, player, sym)
            game.display(board)
            info = winning_info()
            print(info)
            if info == 'over':
                return 'over'
            client.send("valid move".encode())
            break
        else: player = client.send("Invalid move".encode())



for i in range(9):
    result = game_loop(players[i%2][0], symbols[i%2])
    if result == 'over':
        break
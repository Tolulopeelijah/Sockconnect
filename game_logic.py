board = ['#']* 9
game_name = 'Tic-Tac-Toe'

def display(board):
    print('\n' + '-'*13, end = '\n| ')
    for index, val in enumerate(board):
        print(val, end = ' | ')
        if not (index+1) % 3 and index != 8:
            print('\n' + '-'*13, end = '\n| ')
    print('\n' + '-'*13)
    
def validate(board, move)->bool:
    try:
        move = int(move)
    except:
        return False
    return board[move] == '#'

def check_win(board)->['draw', 'X', 'O']:
    winning_positions = ['012', '345', '678', '036', '147', '258', '048', '246']
    if '#' not in board:
        return 'draw'
    for pos in winning_positions:
        X_wins = []
        Y_wins = []
        for i in pos:
            X_wins.append(board[int(i)] == 'X')
            Y_wins.append(board[int(i)] == 'O')
        if all(X_wins): return 'X'
        if all(Y_wins): return 'O'

def update(board, move, player)->['draw', 'X', 'O', 'space taken']: #player enter 1 ahead of index

    move = int(move) - 1
    if validate(board, move):
        board[move-1] = player
    else:
        return 'taken', f'The space has been taken by player {player}'
    
    if check_win(board):
        return check_win(board) 
        print(f'{check_win} won')


    display(board)

def interface(player1, board, label):
    if validate:
        update(board, player1, label)
        

if __name__ == "__main__":
    print('Welcome to the tictactoe game!')
    display(board)
    while not check_win(board):
        for i in ['X', 'O']:
            while (x:= update(board, input(f"{i}'s turn: "), i)):
                if x[0] == 'taken': print('The space has been taken')
                elif x == 'draw': 
                    print('It is a tie!')
                    break
                else: 
                    print(f"{x} won!")
                    break
        display(board)
        
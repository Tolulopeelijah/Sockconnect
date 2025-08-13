board = ['#']* 9

def display(board):
    print('\n' + '-'*13, end = '\n| ')
    for index, val in enumerate(board):
        print(val, end = ' | ')
        if not (index+1) % 3 and index != 8:
            print('\n' + '-'*13, end = '\n| ')
    print('\n' + '-'*13)
    
def validate(board, move)->bool:
    return board[move] == '#'

def check_win(board)->['draw', 'X', 'Y']:
    winning_positions = ['012', '345', '678', '036', '147', '258', '048', '246']
    if '#' not in board:
        return 'draw'
    for pos in winning_positions:
        X_wins = []
        Y_wins = []
        for i in pos:
            X_wins.append(board[int(i)] == 'X')
            Y_wins.append(board[int(i)] == 'Y')
        if all(X_wins): return 'X'
        if all(Y_wins): return 'Y'

def update(board, move, player)->['draw', 'X', 'Y', 'space taken']: #player enter 1 ahead of index
    move = int(move)
    if not validate(board, move-1):
        return 'taken', f'The space has been taken by player {player}'
    board[move-1] = player
    if check_win(board):
        return check_win(board) 
        print(f'{check_win} won')


    display(board)


if __name__ == "__main__":
    print('Welcome to the tictactoe game!')
    display(board)
    while not check_win(board):
        for i in ['X', 'Y']:
            while (x:= update(board, input(f"{i}'s turn: "), i)):
                if x[0] == 'taken': print('The space has been taken')
                elif x == 'draw': 
                    print('It is a tie!')
                    break
                else: 
                    print(f"{x} won!")
                    break
        display(board)
        
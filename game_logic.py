board = ['#']* 9


def display(board):
    print('\n' + '-'*13, end = '\n| ')
    for index, val in enumerate(board):
        print(val, end = ' | ')
        if not (index+1) % 3 and index != 8:
            print('\n' + '-'*13, end = '\n| ')
    print('\n' + '-'*13)
    

display(board)
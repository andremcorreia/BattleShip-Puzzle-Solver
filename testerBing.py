import random
import subprocess
import sys

def generate_board():
    board = [['.' for _ in range(10)] for _ in range(10)]
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for ship in ships:
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, 9)
                col = random.randint(0, 10 - ship)
                if all(board[row][c] == '.' for c in range(col, col + ship)):
                    for c in range(col, col + ship):
                        board[row][c] = 'X'
                    break
            else:
                row = random.randint(0, 10 - ship)
                col = random.randint(0, 9)
                if all(board[r][col] == '.' for r in range(row, row + ship)):
                    for r in range(row, row + ship):
                        board[r][col] = 'X'
                    break
    return board

def write_test_file(board):
    with open('botTest.txt', 'w') as f:
        f.write('ROW\t' + '\t'.join(str(sum(row.count('X') for row in board)) for row in board) + '\n')
        f.write('COLUMN\t' + '\t'.join(str(sum(col.count('X') for col in zip(*board))) for col in range(10)) + '\n')
        hints = []
        for row in range(10):
            for col in range(10):
                if board[row][col] == 'X':
                    if row > 0 and board[row - 1][col] == 'X':
                        hints.append((row, col, 'M'))
                    elif col > 0 and board[row][col - 1] == 'X':
                        hints.append((row, col, 'M'))
                    elif row < 9 and board[row + 1][col] == 'X':
                        hints.append((row, col, 'T'))
                    elif col < 9 and board[row][col + 1] == 'X':
                        hints.append((row, col, 'L'))
                    else:
                        hints.append((row, col, 'C'))
                else:
                    hints.append((row, col, 'W'))
        random.shuffle(hints)
        hints = hints[:random.randint(0, 20)]
        f.write(str(len(hints)) + '\n')
        for hint in hints:
            f.write('HINT\t' + '\t'.join(map(str,hint)) + '\n')

while True:
    board = generate_board()
    write_test_file(board)
    result = subprocess.run(['py', 'bimaru.py', '<botTest.txt'], capture_output=True)
    if result.returncode != 0:
        print('RUNTIME ERROR')
        print('Test file:')
        with open('botTest.txt', 'r') as f:
            print(f.read())
        sys.exit()

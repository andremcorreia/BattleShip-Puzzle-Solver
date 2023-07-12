import os
import random
import subprocess
from itertools import product
from typing import List, Tuple
import signal


class Ship:
    def __init__(self, length: int):
        self.length = length

    def __repr__(self):
        return f"Ship({self.length})"


def create_empty_board(size: int) -> List[List[str]]:
    return [[' ' for _ in range(size)] for _ in range(size)]


def is_valid_placement(board: List[List[str]], ship: Ship, row: int, col: int, orientation: str) -> bool:

    if orientation == 'horizontal':
        if col + ship.length > len(board):
            return False
        for i in range(col - 1, col + ship.length + 1):
            for j in range(row - 1, row + 2):
                if 0 <= i < len(board) and 0 <= j < len(board) and board[j][i] != ' ':
                    return False
    else:
        if row + ship.length > len(board):
            return False
        for i in range(row - 1, row + ship.length + 1):
            for j in range(col - 1, col + 2):
                if 0 <= i < len(board) and 0 <= j < len(board) and board[i][j] != ' ':
                    return False

    return True


def place_ship(board: List[List[str]], ship: Ship, row: int, col: int, orientation: str) -> None:

    char = 'M'
    for i in range(ship.length):
        if ship.length > 1:
            if i == 0:
                char = 'L' if orientation == 'horizontal' else 'T'
            elif i == ship.length - 1:
                char = 'R' if orientation == 'horizontal' else 'B'
            else:
                char = 'M'
        else:
            char = 'C'

        if orientation == 'horizontal':
            board[row][col + i] = char
        else:
            board[row + i][col] = char


def generate_board() -> Tuple[List[List[str]], List[int], List[int]]:
    ships = [Ship(4), Ship(3), Ship(3), Ship(2), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]

    board = create_empty_board(10)

    for ship in ships:
        placed = False
        while not placed:
            row, col = random.randint(0, 9), random.randint(0, 9)
            orientation = random.choice(['horizontal', 'vertical'])
            if is_valid_placement(board, ship, row, col, orientation):
                place_ship(board, ship, row, col, orientation)
                placed = True

    row_counts, col_counts = count_ship_parts(board)

    return board, row_counts, col_counts


def count_ship_parts(board: List[List[str]]) -> Tuple[List[int], List[int]]:
    row_counts = [sum([1 for cell in row if cell != ' ']) for row in board]
    col_counts = [sum([1 for row in board if row[col] != ' ']) for col in range(len(board))]
    return row_counts, col_counts


def generate_test_file(board: List[List[str]]) -> str:
    row_counts, col_counts = count_ship_parts(board)
    hint_count = random.randint(0, 20)

    hints = []
    for _ in range(hint_count):
        row, col = random.randint(0, 9), random.randint(0, 9)
        hint_type = board[row][col] if board[row][col] != ' ' else 'W'
        hints.append((row, col, hint_type))

    test_file = f"ROW    {' '.join(map(str, row_counts))}\n"
    test_file += f"COLUMN    {' '.join(map(str, col_counts))}\n"
    test_file += str(hint_count) + '\n'
    for hint in hints:
        test_file += f"HINT    {' '.join(map(str, hint))}\n"

    return test_file


def main() -> None:
    test_count = 0

    def signal_handler(sig, frame):
        print("\nProgram stopped by user.")
        print(f"Total tests run: {test_count}")
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        test_count += 1
        # Keep generating the board until row and column counts sum to 20
        valid_counts = False
        while not valid_counts:
            board, row_counts, col_counts = generate_board()
            if sum(row_counts) == 20 and sum(col_counts) == 20:
                valid_counts = True

        test_file_content = generate_test_file(board)

        with open('botTest.txt', 'w') as f:
            f.write(test_file_content)

        result = subprocess.run(['py', 'bimaru.py'], stdin=open('botTest.txt', 'r'), stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"RUNTIME ERROR encountered ontest #{test_count}:")
            print("Test file content:")
            print(test_file_content)
            print("Runtime error message:")
            print(result.stderr.decode())  # Print the error message
            break


if __name__ == '__main__':
    main()
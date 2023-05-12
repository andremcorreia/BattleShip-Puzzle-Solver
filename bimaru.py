# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

WATER = "w"
HINTWATER = "W"
CIRCLE = "C"
TOP = "T"
MIDDLE = "M"
BOTTOM = "B"
LEFT = "L"
RIGHT = "R"
UNKNOWN = " "
PART = "X"


import numpy as np
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    WATER = "w"
    HINTWATER = "W"
    CIRCLE = "C"
    TOP = "T"
    MIDDLE = "M"
    BOTTOM = "B"
    LEFT = "L"
    RIGHT = "R"
    UNKNOWN = " "
    PART = "X"

    def __init__(self):
        self.board = np.full((10, 10), self.UNKNOWN)
        self.row_values = []
        self.col_values = []
        self.ships = [4, 3, 2, 1]

    def get_value(self, row: int, col: int) -> str:
        return self.board[row][col]        
    
    def set_value(self, row: int, col: int, value) -> str:
        self.board[row][col] = value
        
    def adjacent_vertical_values(self, row: int, col: int):# -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        res = []
        if row != 0: 
            res += [self.get_value(row - 1, col)]
        if row != 9:
            res += [self.get_value(row + 1, col)]
        return res

    def adjacent_horizontal_values(self, row: int, col: int):# -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        res = []
        if col != 0: 
            res += [self.get_value(row, col - 1)]
        if col != 9:
            res += [self.get_value(row, col + 1)]
        return res

    def get_diagonal_values(self, row: int, col: int):
        res = []
        if col != 0: 
            if row != 0:
                res += [self.board[row-1][col-1]]
            if row != 9:
                res += [self.board[row-1][col-1]]
        if col != 9:
            if row != 0:
                res += [self.board[row-1][col+1]]
            if row != 9:
                res += [self.board[row+1][col+1]]
        return res
    
    def fill_water_row(self, row: int):
        self.board[row] = [self.WATER if value == self.UNKNOWN else value for value in self.board[row]]
    
    def fill_ships_row(self, row: int):
        self.board[row] = [self.assign(row, i, PART) if self.board[row][i] == self.UNKNOWN else self.board[row][i] for i in range(0,10)]

    def fill_water_col(self, col: int):
        for i in range(10):
            if self.board[i][col] == self.UNKNOWN:
                self.board[i][col] = self.WATER
    
    def fill_ships_col(self, col: int):
        for i in range(10):
            if self.board[i][col] == self.UNKNOWN:
                self.assign(i,col,PART)
    
    def wetDiagonals(self, row: int, col: int):
        if col != 0: 
            if row != 0:
                self.board[row-1][col-1] = WATER
            if row != 9:
                self.board[row+1][col-1] = WATER
        if col != 9:
            if row != 0:
                self.board[row-1][col+1] = WATER
            if row != 9:
                self.board[row+1][col+1] = WATER
        return 
    
    def wetVerticaly(self, row: int, col: int):
        if row != 0: 
            self.board[row-1][col] = WATER
        if row != 9:
            self.board[row+1][col] = WATER
        return
    
    def wetSideways(self, row: int, col: int):
        if col != 0: 
            self.board[row][col-1] = WATER
        if col != 9:
            self.board[row][col+1] = WATER
        return
    
    def assign(self,  row: int, col: int, type: str):
        print("assigned", row, col, type)
        if row < 0 or row > 9 or col < 0 or col > 9:
            return
        if self.board[row][col] != UNKNOWN and self.board[row][col] != type:
            return False
        if type != WATER and type != HINTWATER:
            self.wetDiagonals(row, col)
        if type == CIRCLE:
            self.wetVerticaly(row, col)
            self.wetSideways(row, col)
        if type == TOP:
            self.wetSideways(row, col)
            if row != 0: 
                self.set_value(row - 1, col, WATER)
            self.assign(row+1, col, PART)
        if type == BOTTOM:
            self.wetSideways(row, col)
            if row != 9: 
                self.set_value(row + 1, col, WATER)
            self.assign(row-1, col, PART)
        if type == RIGHT:
            self.wetVerticaly(row, col)
            if col != 9: 
                self.set_value(row, col + 1, WATER)
            self.assign(row, col-1, PART)
        if type == LEFT:
            self.wetVerticaly(row, col)
            if col != 0: 
                self.set_value(row, col - 1, WATER)
            self.assign(row, col+1, PART)
        self.set_value(row, col, type)

    def lineProcesser(self):
        modified = False
        for i in range(0,10):
            rowShips, colShips, rowEmpty, colEmpty = 0,0,0,0
            for j in range(0,10):
                if self.board[i][j] == UNKNOWN:
                    rowEmpty += 1
                elif self.board[i][j] != WATER and self.board[i][j] != HINTWATER:
                    rowShips += 1
                if self.board[j][i] == UNKNOWN:
                    colEmpty += 1
                elif self.board[j][i] != WATER and self.board[j][i] != HINTWATER:
                    colShips += 1

                if self.board[i][j] == MIDDLE:
                    adjH = self.adjacent_horizontal_values(i,j)
                    adjV = self.adjacent_vertical_values(i,j)
                    if WATER in adjH or HINTWATER in adjH or len(adjH) == 1:
                        if UNKNOWN in adjV:
                            print(adjV)
                            modified = True
                            self.assign(i-1,j,PART)
                            self.assign(i+1,j,PART)
                    
                    if WATER in adjV or HINTWATER in adjV or len(adjV) == 1:
                        if UNKNOWN in adjH:
                            print(adjH)
                            modified = True
                            self.assign(i,j-1,PART)
                            self.assign(i,j+1,PART)

            if rowShips == self.row_values[i] and rowEmpty != 0:
                modified = True
                self.fill_water_row(i)
            elif rowShips + rowEmpty == self.row_values[i] and rowEmpty != 0:
                modified = True
                self.fill_ships_row(i)
            if colShips == self.col_values[i] and colEmpty != 0:
                modified = True
                self.fill_water_col(i)
            elif colShips + colEmpty == self.col_values[i]  and colEmpty != 0:
                modified = True
                self.fill_ships_col(i)
        if modified:
            self.lineProcesser()

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        board = Board()
        filename = sys.argv[1]
        with open(filename) as f:
            lines = f.readlines()
        # Parse the row and column values
        board.row_values = list(map(int, lines[0].split()[1:]))
        board.col_values = list(map(int, lines[1].split()[1:]))
        # Parse the hints and place them on the board
        for line in lines[3:]:
            input = line.split()
            row, col = int(input[1]), int(input[2])
            letter = input[3]
            board.assign(row,col,letter)
        return board
    
class BimaruState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, board: Board):
        originalState = BimaruState(board)
        print("input")
        print(board.board)
        board.lineProcesser()
        print("simplified")
        print(board.board)
        print(board.row_values)
        print(board.col_values)
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    originalBoard = Board.parse_instance()
    game = Bimaru(originalBoard)
    pass

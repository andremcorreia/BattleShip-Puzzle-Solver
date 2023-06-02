# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 12:
# 102666 André Correia
# 103333 João Trocado

import copy
import numpy as np
from sys import stdin
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
    WATER       = "."
    HINTWATER   = "W"
    CIRCLE      = "c"
    TOP         = "t"
    MIDDLE      = "m"
    BOTTOM      = "b"
    LEFT        = "l"
    RIGHT       = "r"
    UNKNOWN     = "?"
    PART        = "x"
    SHIP_TILES  = {PART,RIGHT,LEFT,BOTTOM,MIDDLE,TOP,CIRCLE}
    WATER_TILES = {WATER,HINTWATER}
    VERTICAL    = "VERTICAL"
    HORIZONTAL  = "HORIZONTAL"

    def __init__(self):
        self.board = np.full((10, 10), self.UNKNOWN)
        self.row_values = [] 
        self.col_values = []
        self.ships = [4, 3, 2, 1] # Available ships
        self.isLegal = True
        self.row_available = np.zeros(10) # Data for action finder
        self.col_available = np.zeros(10) # Data for action finder

    def isShip(self, row: int, col: int) -> bool:
        return self.board[row,col].lower() in self.SHIP_TILES
    
    def isWater(self, row: int, col: int) -> bool:
        return self.board[row,col] in self.WATER_TILES

    def get_value(self, row: int, col: int) -> str:
        return self.board[row,col].lower()        
    
    def set_value(self, row: int, col: int, value):
        if self.board[row,col] != self.HINTWATER:
            self.board[row,col] = value
        
    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        res = []
        if row != 0: 
            res += [self.get_value(row - 1, col)]
        if row != 9:
            res += [self.get_value(row + 1, col)]
        return res

    def adjacent_horizontal_values(self, row: int, col: int):
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
        self.board[row, self.board[row] == self.UNKNOWN] = self.WATER
    
    def fill_ships_row(self, row: int):
        for c in range(10):
            if self.board[row, c] == self.UNKNOWN:
                self.assign(row, c, self.PART)

    def fill_water_col(self, col: int):
        self.board[self.board[:, col] == self.UNKNOWN, col] = self.WATER
    
    def fill_ships_col(self, col: int):
        for i in range(10):
            if self.board[i, col] == self.UNKNOWN:
                self.assign(i,col, self.PART)
    
    def water_diagonals(self, row: int, col: int):
        if col != 0:
            if row != 0 and self.board[row-1, col-1] != self.HINTWATER:
                self.board[row-1, col-1] = self.WATER
            if row != 9 and self.board[row+1, col-1] != self.HINTWATER:
                self.board[row+1, col-1] = self.WATER
        if col != 9:
            if row != 0 and self.board[row-1, col+1] != self.HINTWATER:
                self.board[row-1, col+1] = self.WATER
            if row != 9 and self.board[row+1, col+1] != self.HINTWATER:
                self.board[row+1, col+1] = self.WATER
    
    def water_adjacent_vertical(self, row: int, col: int):
        if row != 0 and self.board[row-1, col] != self.HINTWATER:
            self.board[row-1, col] = self.WATER
        if row != 9 and self.board[row+1, col] != self.HINTWATER:
            self.board[row+1, col] = self.WATER

    def water_adjacent_horizontal(self, row: int, col: int):
        if col != 0 and self.board[row, col-1] != self.HINTWATER:
            self.board[row, col-1] = self.WATER
        if col != 9 and self.board[row, col+1] != self.HINTWATER:
            self.board[row, col+1] = self.WATER
    
    def assign(self,  row: int, col: int, type: str):
        if row < 0 or row > 9 or col < 0 or col > 9:
            return
        if (type == self.HINTWATER):
            self.set_value(row, col, type)
            return
        
        if self.board[row,col] != self.UNKNOWN and self.board[row,col] != type and not type.isupper():
            return False
        
        if type.lower() != self.WATER and type != self.HINTWATER:
            self.water_diagonals(row, col)

        if type.lower() == self.CIRCLE:
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_horizontal(row, col)

        if type.lower() == self.TOP:
            self.water_adjacent_horizontal(row, col)
            if row != 0: 
                self.set_value(row - 1, col, self.WATER)
            self.assign(row+1, col, self.PART)

        if type.lower() == self.BOTTOM:
            self.water_adjacent_horizontal(row, col)
            if row != 9: 
                self.set_value(row + 1, col, self.WATER)
            self.assign(row-1, col, self.PART)

        if type.lower() == self.RIGHT:
            self.water_adjacent_vertical(row, col)
            if col != 9: 
                self.set_value(row, col + 1, self.WATER)
            self.assign(row, col-1, self.PART)

        if type.lower() == self.LEFT:
            self.water_adjacent_vertical(row, col)
            if col != 0: 
                self.set_value(row, col - 1, self.WATER)
            self.assign(row, col+1, self.PART)
        self.set_value(row, col, type)

    def biggest_size_available(self) -> int: #?
        last = 0 
        for i in range(4):
            if self.ships[i] > 0:
                last = i
        return last + 1

    def boardSimplifier(self):
        if(not self.isLegal):
            return
        modified = False
        self.shipCount()
        max = self.biggest_size_available()
        for i in range(10):
            rowShips, colShips, rowEmpty, colEmpty, rowStreak, colStreak = 0,0,0,0,0,0
            for j in range(10):
                #Part Definer
                if self.board[i,j].lower() == self.PART and self.UNKNOWN not in self.adjacent_horizontal_values(i,j) + self.adjacent_vertical_values(i,j):
                    top     = i == 0 or self.isWater(i-1, j)
                    bottom  = i == 9 or self.isWater(i+1, j)
                    right   = j == 9 or self.isWater(i, j+1)
                    left    = j == 0 or self.isWater(i, j-1)
                    if top and not bottom:
                        self.board[i,j] = self.TOP
                        modified = True
                    elif bottom and not top:
                        self.board[i,j] = self.BOTTOM
                    elif right and not left:
                        self.board[i,j] = self.RIGHT 
                    elif left and not right:
                        self.board[i,j] = self.LEFT
                        modified = True
                    elif left and right and top and bottom:
                        self.board[i,j] = self.CIRCLE
                    elif (left and right) or (top and bottom):
                        self.board[i,j] = self.MIDDLE
                #end

                #Row
                if self.board[i,j] == self.UNKNOWN:
                    rowStreak = 0
                    rowEmpty += 1
                elif self.board[i,j] not in self.WATER_TILES:
                    rowStreak += 1
                    rowShips += 1
                else:
                    rowStreak = 0

                if rowStreak == max and (j == 9 or self.board[i,j + 1] in [self.UNKNOWN, self.WATER, self.HINTWATER]) and (j == 0 or self.board[i, j - max] in [self.UNKNOWN, self.WATER, self.HINTWATER]):
                    check = []
                    if j + 1 < 10:
                        check += self.board[i,j + 1]
                    if j - max >= 0:
                        check += self.board[i, j - max]

                    if self.UNKNOWN in check:                    
                        self.assign(i, j + 1, self.WATER)
                        self.assign(i, j - max, self.WATER)
                        modified = True

                #Col
                if self.board[j,i].lower() == self.UNKNOWN:
                    colStreak = 0
                    colEmpty += 1
                elif self.board[j,i] not in self.WATER_TILES:
                    colStreak += 1
                    colShips += 1
                else:
                    colStreak = 0

                if colStreak == max and (j == 9 or self.board[j + 1, i] in [self.UNKNOWN, self.WATER, self.HINTWATER]) and (j == 0 or self.board[j - max, i] in [self.UNKNOWN, self.WATER, self.HINTWATER]):
                    check = []
                    if j + 1 < 10:
                        check += self.board[j + 1, i]
                    if j - max >= 0:
                        check += self.board[j - max, i]
                    if self.UNKNOWN in check:
                        self.assign(j + 1, i, self.WATER)
                        self.assign(j - max, i, self.WATER)
                        modified = True

                # M Solver
                if self.board[i,j].lower() == self.MIDDLE:
                    adjH = self.adjacent_horizontal_values(i,j)
                    adjV = self.adjacent_vertical_values(i,j)
                    if self.WATER in adjH or self.HINTWATER in adjH or len(adjH) == 1:
                        if self.UNKNOWN in adjV:
                            modified = True
                            self.assign(i-1,j, self.PART)
                            self.assign(i+1,j, self.PART)
                    
                    if self.WATER in adjV or self.HINTWATER in adjV or len(adjV) == 1:
                        if self.UNKNOWN in adjH:
                            modified = True
                            self.assign(i,j-1, self.PART)
                            self.assign(i,j+1, self.PART)

            # Filler Row    
            if rowShips == self.row_values[i] and rowEmpty != 0:
                modified = True
                self.fill_water_row(i)
            elif rowShips + rowEmpty == self.row_values[i] and rowEmpty != 0:
                modified = True
                self.fill_ships_row(i)

            # Filler Col  
            if colShips == self.col_values[i] and colEmpty != 0:
                modified = True
                self.fill_water_col(i)
            elif colShips + colEmpty == self.col_values[i]  and colEmpty != 0:
                modified = True
                self.fill_ships_col(i)

            if self.row_values[i] > rowShips + rowEmpty or self.row_values[i] < rowShips:
                self.isLegal = False
            if self.col_values[i] > colShips + colEmpty or self.col_values[i] < colShips:
                self.isLegal = False

            self.row_available[i] = self.row_values[i] - rowShips
            self.col_available[i] = self.col_values[i] - colShips
            
        if modified and self.isLegal:
            self.boardSimplifier()

    def shipCount(self):
        # Counts all ships in the board
        self.ships = [4, 3, 2, 1]
        for row in range(10):
            for col in range(10):
                if self.get_value(row,col).lower() == self.CIRCLE:
                    self.ships[0] -= 1 

                if self.get_value(row,col).lower() == self.LEFT:
                    i = 1
                    while (col + i < 10 and self.isShip(row,col + i) and i < 4):
                        i += 1
                    if (col + i == 10 or self.isWater(row,col + i)):
                        self.ships[i - 1] -= 1

                if self.get_value(row,col).lower() == self.TOP:
                    i = 1
                    while (row + i < 10 and self.isShip(row + i,col) and i < 4):
                        i += 1
                    if (row + i == 10 or self.isWater(row + i,col)):
                        self.ships[i - 1] -= 1
    
    def actionFinder(self, boatSize: int):
        # Finds possible positions for ships
        if(not self.isLegal):
            return []
        res = []
        if boatSize > 1:
            for i in range(10):
                for j in range(10):
                    #Check rows for available spots
                    alreadyIn = 0
                    if (self.get_value(i,j) == self.UNKNOWN or self.isShip(i,j)):
                        if self.get_value(i,j) != self.UNKNOWN:
                            alreadyIn += 1
                        c, reached = 1, False
                        while (j + c < 10 and (self.get_value(i,j + c) == self.UNKNOWN or self.isShip(i,j + c)) and not reached):
                            if self.get_value(i,j + c) != self.UNKNOWN:
                                alreadyIn += 1
                            c += 1
                            if c >= boatSize:
                                reached = True
                                if ((j + c == 10 or not self.isShip(i,j + c)) and (j == 0 or not self.isShip(i, j - 1)) and (self.get_value(i,j) == self.UNKNOWN or self.get_value(i,j + c-1) == self.UNKNOWN or alreadyIn < c) and self.row_available[i] >= boatSize - alreadyIn):
                                    res += [[i,j,self.HORIZONTAL,boatSize]]
                    #Check Collums for available spots
                    if self.get_value(j,i) == self.UNKNOWN or self.isShip(j,i):
                        if self.get_value(j,i) != self.UNKNOWN:
                            alreadyIn += 1
                        c, reached = 1, False
                        while (j + c < 10 and (self.get_value(j + c,i) == self.UNKNOWN or self.isShip(j + c,i)) and not reached):
                            if self.get_value(j + c,i) != self.UNKNOWN:
                                alreadyIn += 1
                            c += 1
                            if c >= boatSize:
                                reached = True
                                if ((j + c == 10 or not self.isShip(j + c,i)) and (j == 0 or not self.isShip(j - 1,i)) and (self.get_value(j,i) == self.UNKNOWN or self.get_value(j + c-1,i) == self.UNKNOWN or alreadyIn < c) and self.col_available[i] >= boatSize - alreadyIn):
                                    res += [[j,i,self.VERTICAL,boatSize]]
        if boatSize == 1:
            for i in range(10):
                for j in range(10):
                    #Check rows for available spots
                    alreadyIn = 0
                    if (self.get_value(i,j) == self.UNKNOWN):
                        res += [[i,j,self.HORIZONTAL,boatSize]]
        return res
    
    def addShip(self, shipInfo):
        # Adds an entire ship on the board
        if (shipInfo[2] == self.HORIZONTAL):
            for i in range(0, shipInfo[3]):
                self.assign(shipInfo[0], shipInfo[1] + i, self.PART)
            self.assign(shipInfo[0], shipInfo[1] - 1, self.WATER)
            self.assign(shipInfo[0], shipInfo[1] + shipInfo[3], self.WATER)
        if (shipInfo[2] == self.VERTICAL):
            for i in range(0, shipInfo[3]):
                self.assign(shipInfo[0] + i, shipInfo[1], self.PART)
            self.assign(shipInfo[0] - 1, shipInfo[1], self.WATER)
            self.assign(shipInfo[0] + shipInfo[3], shipInfo[1], self.WATER)
    
    def __str__(self):
        res = ""
        for i, row in enumerate(self.board):
            for value in row:
                res += value
            if i < len(self.board) - 1:
                res += "\n"
        return res

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        board = Board()
        lines = stdin.readlines()
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
    
class Bimaru(Problem):
    def __init__(self, originalBoard: Board):
        self.initial = BimaruState(originalBoard)
        self.originalBoard = originalBoard

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if (not state.board.isLegal):
            return []
        
        state.board.shipCount()

        for size in (4,3,2,1):
            if state.board.ships[size - 1] > 0:
                return state.board.actionFinder(size)
        return []

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        newState = BimaruState(copy.deepcopy(state.board))
        newState.board.addShip(action)
        return newState
        

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        state.board.boardSimplifier()
        state.board.shipCount()
        return state.board.ships == [0,0,0,0] and state.board.isLegal

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass


if __name__ == "__main__":
    originalBoard = Board.parse_instance()
    game = Bimaru(originalBoard)
    finalNode = depth_first_tree_search(game)
    print(finalNode.state.board)




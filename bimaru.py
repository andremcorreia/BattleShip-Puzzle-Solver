# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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
    WATER       = " "
    HINTWATER   = "W"
    CIRCLE      = "C"
    TOP         = "T"
    MIDDLE      = "M"
    BOTTOM      = "B"
    LEFT        = "L"
    RIGHT       = "R"
    UNKNOWN     = "?"
    PART        = "x"
    SHIP_TILES  = [PART,RIGHT,LEFT,BOTTOM,MIDDLE,TOP,CIRCLE]
    WATER_TILES = [WATER,HINTWATER]
    VERTICAL    = "VERTICAL"
    HORIZONTAL  = "HORIZONTAL"

    def __init__(self):
        self.board = np.full((10, 10), self.UNKNOWN)
        self.row_values = []
        self.col_values = []
        self.ships = [4, 3, 2, 1]
        self.isLegal = True
        self.times = 0

    def isShip(self, row: int, col: int):
        return self.board[row][col] in self.SHIP_TILES
    
    def isWater(self, row: int, col: int):
        return self.board[row][col] in self.WATER_TILES

    def get_value(self, row: int, col: int) -> str:
        return self.board[row][col].upper()        
    
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
        for c in range(1,10):
            if self.board[row][c] == self.UNKNOWN:
                self.assign(row, c, self.PART)

    def fill_water_col(self, col: int):
        for i in range(10):
            if self.board[i][col] == self.UNKNOWN:
                self.board[i][col] = self.WATER
    
    def fill_ships_col(self, col: int):
        for i in range(10):
            if self.board[i][col] == self.UNKNOWN:
                self.assign(i,col, self.PART)
    
    def wetDiagonals(self, row: int, col: int):
        if col != 0: 
            if row != 0:
                self.board[row-1][col-1] = self.WATER
            if row != 9:
                self.board[row+1][col-1] = self.WATER
        if col != 9:
            if row != 0:
                self.board[row-1][col+1] = self.WATER
            if row != 9:
                self.board[row+1][col+1] = self.WATER
        return 
    
    def wetVerticaly(self, row: int, col: int):
        if row != 0: 
            self.board[row-1][col] = self.WATER
        if row != 9:
            self.board[row+1][col] = self.WATER
        return
    
    def wetSideways(self, row: int, col: int):
        if col != 0: 
            self.board[row][col-1] = self.WATER
        if col != 9:
            self.board[row][col+1] = self.WATER
        return
    
    def assign(self,  row: int, col: int, type: str):
        if row < 0 or row > 9 or col < 0 or col > 9:
            return
        if self.board[row][col] != self.UNKNOWN and self.board[row][col] != type:
            return False
        if type != self.WATER and type != self.HINTWATER:
            self.wetDiagonals(row, col)
        if type == self.CIRCLE:
            self.wetVerticaly(row, col)
            self.wetSideways(row, col)
        if type == self.TOP:
            self.wetSideways(row, col)
            if row != 0: 
                self.set_value(row - 1, col, self.WATER)
            self.assign(row+1, col, self.PART)
        if type == self.BOTTOM:
            self.wetSideways(row, col)
            if row != 9: 
                self.set_value(row + 1, col, self.WATER)
            self.assign(row-1, col, self.PART)
        if type == self.RIGHT:
            self.wetVerticaly(row, col)
            if col != 9: 
                self.set_value(row, col + 1, self.WATER)
            self.assign(row, col-1, self.PART)
        if type == self.LEFT:
            self.wetVerticaly(row, col)
            if col != 0: 
                self.set_value(row, col - 1, self.WATER)
            self.assign(row, col+1, self.PART)
        self.set_value(row, col, type)

    def lineProcesser(self):
        modified = False
        for i in range(0,10):
            rowShips, colShips, rowEmpty, colEmpty = 0,0,0,0
            for j in range(0,10):

                #Part Definer
                if self.board[i][j] == self.PART and self.UNKNOWN not in self.adjacent_horizontal_values(i,j) + self.adjacent_vertical_values(i,j):
                    top     = i == 0 or self.isWater(i-1, j)
                    bottom  = i == 9 or self.isWater(i+1, j)
                    right   = j == 9 or self.isWater(i, j+1)
                    left    = j == 0 or self.isWater(i, j-1)
                    if top and not bottom:
                        self.board[i][j] = self.TOP
                    elif bottom and not top:
                        self.board[i][j] = self.BOTTOM
                    elif right and not left:
                        self.board[i][j] = self.RIGHT 
                    elif left and not right:
                        self.board[i][j] = self.LEFT
                    elif left and right and top and bottom:
                        self.board[i][j] = self.CIRCLE
                    elif (left and right) or (top and bottom):
                        self.board[i][j] = self.MIDDLE
                #end

                #Row
                if self.board[i][j] == self.UNKNOWN:
                    rowEmpty += 1
                elif self.board[i][j] not in self.WATER_TILES:
                    rowShips += 1
                #Col
                if self.board[j][i] == self.UNKNOWN:
                    colEmpty += 1
                elif self.board[j][i] not in self.WATER_TILES:
                    colShips += 1

                # M Solver
                if self.board[i][j] == self.MIDDLE:
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

            #Illegal check
            if self.row_values[i] > rowShips + rowEmpty:
                self.isLegal = False
                print("DEAD END")
            if self.col_values[i] > colShips + colEmpty:
                self.isLegal = False
                print("DEAD END")
            
        if modified and self.isLegal:
            self.lineProcesser()

    def shipCount(self):
        self.ships = [4, 3, 2, 1]
        for row in range(0,10):
            for col in range(0,10):
                if self.get_value(row,col) == self.CIRCLE.upper():
                    self.ships[0] -= 1 
                if self.get_value(row,col) == self.LEFT.upper():
                    i = 1
                    while (not self.isWater(row,col + i)):
                        i += 1
                    self.ships[i - 1] -= 1
                if self.get_value(row,col) == self.TOP.upper():
                    i = 1
                    while (not self.isWater(row + i,col)):
                        i += 1
                    self.ships[i - 1] -= 1
    
    def guess_finder(self, boatSize: int):
        if(not self.isLegal):
            return []
        res = []
        for i in range(0, 10):
            for j in range(0, 10):
                #Check rows for available spots
                if self.get_value(i,j) in [self.UNKNOWN, self.PART]:
                    c, reached = 1, False
                    while (self.get_value(i,j + c) in [self.UNKNOWN, self.PART] and not reached):
                        c += 1
                        if c >= boatSize:
                            reached = True
                            res += [[i,j,self.HORIZONTAL,boatSize]]
                #Check Collums for available spots
                if self.get_value(j,i) in [self.UNKNOWN, self.PART]:
                    c, reached = 1, False
                    while (self.get_value(j + c,i) in [self.UNKNOWN, self.PART] and not reached):
                        c += 1
                        if c >= boatSize:
                            reached = True
                            res += [[j,i,self.VERTICAL,boatSize]]
        return res
    
    def addShip(self, shipInfo):
        if (shipInfo[2] == self.HORIZONTAL):
            print(shipInfo[3])
            for i in range(0, shipInfo[3]):
                self.assign(shipInfo[0], shipInfo[1] + i, self.PART)
        if (shipInfo[2] == self.VERTICAL):
            for i in range(0, shipInfo[3]):
                self.assign(shipInfo[0] + i, shipInfo[1], self.PART)

    def print_board(self):
        print(self.board)
        
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        board = Board()
        #with open('t1.txt', 'r') as file:
        #    lines = file.readlines()
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

    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, originalBoard: Board):
        self.initial = BimaruState(originalBoard)
        self.initial.board.lineProcesser()
        self.originalBoard = originalBoard

        #print("input")
        #print(originalBoard.board)
        #originalBoard.lineProcesser()
        #print("simplified")
        #originalBoard.print_board()
        #print(originalBoard.row_values) 
        #print(originalBoard.col_values)
#
#
        #originalBoard.shipCount()
        #print("remaining ships:", originalBoard.ships)
        #if (originalBoard.ships[3] > 0):
        #    print("next guesses:", originalBoard.guess_finder(4))
        #elif (originalBoard.ships[2] > 0):
        #    print("next guesses:", originalBoard.guess_finder(3))    
        #elif (originalBoard.ships[1] > 0):
        #    print("next guesses:", originalBoard.guess_finder(2))  
        #elif (originalBoard.ships[0] > 0):
        #    print("next guesses:", originalBoard.guess_finder(1))                          
        

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        state.board.shipCount()
        print("remaining ships:", state.board.ships)
        print(state.board.board)
        if (state.board.ships[3] > 0):
            print(state.board.guess_finder(4))
            return state.board.guess_finder(4) 
        elif (state.board.ships[2] > 0):
            print(state.board.guess_finder(3))
            return state.board.guess_finder(3)     
        elif (state.board.ships[1] > 0):
            print(state.board.guess_finder(2))
            return state.board.guess_finder(2)  
        elif (state.board.ships[0] > 0):
            print(state.board.guess_finder(1))
            return state.board.guess_finder(1) 

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        print("resulting")
        print(action)
        newState = BimaruState(copy.deepcopy(state.board))
        newState.board.addShip(action)
        newState.board.lineProcesser()
        print(newState.board.print_board())
        return newState
        # [row,col,sentido]
        # new state
        # addShip(row,col,direction)
        # line process
        # remove from action list
        # return state        

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.ships == [0,0,0,0] and state.board.isLegal

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
    print("yay1")
    print(depth_first_tree_search(game).state)
    print("yay2")


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

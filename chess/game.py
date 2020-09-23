import pygame
from .board import Board
from .constants import WHITE, BLACK, KING, CASTLE

class Game:
    def __init__(self, win):
        self.win = win
        self._init()
    
    def _init(self):
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.viable_moves = {}  # (row, col): move/take/guard

    def reset(self):
        self._init()

    def update(self):
        self.board.draw(self.win, self.viable_moves)
        pygame.display.update()

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def select(self, row, col):
        if self.selected:
            if (row, col) in self.viable_moves:
                # check that selected move leaves us in a non-check state
                if self.board.check_move(self.selected, (row, col)):
                    # move piece to selected square
                    if self.viable_moves[(row, col)] == CASTLE:
                        self.board.castle(self.selected, row, col)
                    else:
                        self.board.move(self.selected, row, col, self.win)
                    self.change_turn()
                else:
                    self.selected = None
                    self.viable_moves = {}
        
        if self.board.board[row][col] != 0 and self.board.board[row][col].colour == self.turn:
            self.selected = self.board.board[row][col]
            self.viable_moves = self.board.get_viable_moves(self.selected)

            delete = [key for key in self.viable_moves if not self.board.check_move(self.selected, key)]
            for key in delete: del self.viable_moves[key]
        else:
            self.selected = None
            self.viable_moves = {}
    
    def stalemate(self):
        if self.board.stalemate(self.turn):
            return True
        else:
            return False

    def checkmate(self):
        if self.board.in_check(self.turn) and self.board.checkmate(self.turn):
            return True
        else:
            return False
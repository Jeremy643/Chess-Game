import pygame
from itertools import product
from .constants import SQUARE_SIZE, WHITE, BLACK, MOVE, TAKE, CASTLE, GUARD, WHITE_PAWN, BLACK_PAWN, PAWN, WHITE_KNIGHT, BLACK_KNIGHT, KNIGHT, WHITE_BISHOP, BLACK_BISHOP, BISHOP, \
WHITE_ROOK, BLACK_ROOK, ROOK, WHITE_QUEEN, BLACK_QUEEN, QUEEN, WHITE_KING, BLACK_KING, KING

class Piece:
    def __init__(self, row, col, colour, piece_type):
        self.row = row
        self.col = col
        self.colour = colour
        self.piece_type = piece_type

        if self.colour == WHITE and self.piece_type == PAWN:
            self.direction = -1
        elif self.colour == BLACK and self.piece_type == PAWN:
            self.direction = 1
        else:
            self.direction = None

        self.moved = False  # for castling
        self.x = 0
        self.y = 0
        self._calc_pos()
    
    def _calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
    
    def _search_route(self, board, inc):
        # function used by bishop, rook and queen pieces
        viable_moves = {}
        for i in inc:
                row_mult, col_mult = i
                index = 1
                while True:
                    r = index * row_mult
                    c = index * col_mult
                    if 0 <= self.row + r <= 7 and 0 <= self.col + c <= 7:
                        sq = board[self.row + r][self.col + c]
                        if sq == 0:
                            viable_moves[(self.row + r, self.col + c)] = MOVE
                            index += 1
                        elif sq != 0 and sq.colour != self.colour:
                            viable_moves[(self.row + r, self.col + c)] = TAKE
                            break
                        elif sq != 0 and sq.colour == self.colour:
                            viable_moves[(self.row + r, self.col + c)] = GUARD
                            break
                    else:
                        break
        return viable_moves
    
    def get_possible_moves(self, board):
        viable_moves = {}
        if self.piece_type == PAWN:
            if (self.row == 6 and self.colour == WHITE) or (self.row == 1 and self.colour == BLACK):
                # pawn on start row
                for i in range(1, 3):
                    if board[self.row + (self.direction * i)][self.col] == 0:
                        # found possible move
                        viable_moves[(self.row + (self.direction * i), self.col)] = MOVE
                    else:
                        # piece in the way
                        break
            else:
                # can only move forward 1 square
                if 0 <= self.row + (self.direction * 1) <= 7 and board[self.row + (self.direction * 1)][self.col] == 0:
                    # found possible move
                    viable_moves[(self.row + (self.direction * 1), self.col)] = MOVE
            
            # check potential takes or guards
            if 0 <= self.row + (self.direction * 1) <= 7:
                if (self.col - 1) >= 0 and (board[self.row + (self.direction * 1)][self.col - 1] == 0 or board[self.row + (self.direction * 1)][self.col - 1].colour == self.colour):
                    viable_moves[(self.row + (self.direction * 1), self.col - 1)] = GUARD
                elif (self.col - 1) >= 0 and board[self.row + (self.direction * 1)][self.col - 1].colour != self.colour:
                    viable_moves[(self.row + (self.direction * 1), self.col - 1)] = TAKE

                if (self.col + 1) <= 7 and (board[self.row + (self.direction * 1)][self.col + 1] == 0 or board[self.row + (self.direction * 1)][self.col + 1].colour == self.colour):
                    viable_moves[(self.row + (self.direction * 1), self.col + 1)] = GUARD
                elif (self.col + 1) <= 7 and board[self.row + (self.direction * 1)][self.col + 1].colour != self.colour:
                    viable_moves[(self.row + (self.direction * 1), self.col + 1)] = TAKE
        elif self.piece_type == KNIGHT:
            prod = list(product((2, 1, -1, -2), repeat=2))
            delete = []
            for p in prod:
                r, c = p
                if abs(r) == abs(c):
                    delete.append(p)
            prod = [p for p in prod if p not in delete]
            
            # remove moves that are off the board
            possible_moves = []
            for p in prod:
                r, c = p
                if 0 <= self.row + r <= 7 and 0 <= self.col + c <= 7:
                    possible_moves.append(p)
            
            # find if its a move or a take
            for move in possible_moves:
                r, c = move
                if board[self.row + r][self.col + c] == 0:
                    viable_moves[(self.row + r, self.col + c)] = MOVE
                elif board[self.row + r][self.col + c] != 0 and self.colour != board[self.row + r][self.col + c].colour:
                    viable_moves[(self.row + r, self.col + c)] = TAKE
                elif board[self.row + r][self.col + c] != 0 and self.colour == board[self.row + r][self.col + c].colour:
                    viable_moves[(self.row + r, self.col + c)] = GUARD
        elif self.piece_type == BISHOP:
            prod = list(product((1, -1), repeat=2))
            viable_moves = self._search_route(board, prod)
        elif self.piece_type == ROOK:
            prod = list(product((1, 0, -1), repeat=2))

            # remove incrementors that move along the diagonal
            delete = [key for key in prod if abs(key[0]) == abs(key[1])]
            for d in delete: prod.remove(d)

            viable_moves = self._search_route(board, prod)
        elif self.piece_type == QUEEN:
            prod = list(product((1, 0, -1), repeat=2))
            prod.remove((0, 0))

            viable_moves = self._search_route(board, prod)
        elif self.piece_type == KING:
            # check potential moves and takes
            prod = list(product((1, -1, 0), repeat=2))  # list of tuples to add to row and col to get adjacent squares
            prod.remove((0, 0))
            for p in prod:
                r, c = p
                if 0 <= self.row + r <= 7 and 0 <= self.col + c <= 7:
                    sq = board[self.row + r][self.col + c]
                    if sq == 0:
                        # empty square
                        viable_moves[(self.row + r, self.col + c)] = MOVE
                    elif sq != 0 and sq.colour != self.colour:
                        # enemy piece
                        viable_moves[(self.row + r, self.col + c)] = TAKE
                    elif sq != 0 and sq.colour == self.colour:
                        # friendly piece
                        viable_moves[(self.row + r, self.col + c)] = GUARD
                else:
                    continue
            
            # check for castling on king and queen side
            if not self.moved:
                # check right corner square
                unbroken = True
                for i in range(1, 3):
                    # check no other pieces get in the way
                    if board[self.row][self.col + i] != 0:
                        unbroken = False
                        break
                right_sq = board[self.row][self.col + 3]
                if unbroken and right_sq != 0 and right_sq.colour == self.colour and right_sq.piece_type == ROOK and not right_sq.moved:
                    viable_moves[(self.row, self.col + 2)] = CASTLE
                
                # check left corner square
                unbroken = True
                for i in range(1, 4):
                    # check no other pieces get in the way
                    if board[self.row][self.col - i] != 0:
                        unbroken = False
                        break
                left_sq = board[self.row][self.col - 4]
                if unbroken and left_sq != 0 and left_sq.colour == self.colour and left_sq.piece_type == ROOK and not left_sq.moved:
                    viable_moves[(self.row, self.col - 2)] = CASTLE
    
        return viable_moves
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.moved = True
        self._calc_pos()
    
    def draw(self, win):
        if self.colour == WHITE:
            if self.piece_type == PAWN:
                width, height = WHITE_PAWN.get_rect().size
                win.blit(WHITE_PAWN, (self.x - width//2, self.y - height//2))
            elif self.piece_type == KNIGHT:
                width, height = WHITE_KNIGHT.get_rect().size
                win.blit(WHITE_KNIGHT, (self.x - width//2, self.y - height//2))
            elif self.piece_type == BISHOP:
                width, height = WHITE_BISHOP.get_rect().size
                win.blit(WHITE_BISHOP, (self.x - width//2, self.y - height//2))
            elif self.piece_type == ROOK:
                width, height = WHITE_ROOK.get_rect().size
                win.blit(WHITE_ROOK, (self.x - width//2, self.y - height//2))
            elif self.piece_type == QUEEN:
                width, height = WHITE_QUEEN.get_rect().size
                win.blit(WHITE_QUEEN, (self.x - width//2, self.y - height//2))
            elif self.piece_type == KING:
                width, height = WHITE_KING.get_rect().size
                win.blit(WHITE_KING, (self.x - width//2, self.y - height//2))
        else:
            if self.piece_type == PAWN:
                width, height = BLACK_PAWN.get_rect().size
                win.blit(BLACK_PAWN, (self.x - width//2, self.y - height//2))
            elif self.piece_type == KNIGHT:
                width, height = BLACK_KNIGHT.get_rect().size
                win.blit(BLACK_KNIGHT, (self.x - width//2, self.y - height//2))
            elif self.piece_type == BISHOP:
                width, height = BLACK_BISHOP.get_rect().size
                win.blit(BLACK_BISHOP, (self.x - width//2, self.y - height//2))
            elif self.piece_type == ROOK:
                width, height = BLACK_ROOK.get_rect().size
                win.blit(BLACK_ROOK, (self.x - width//2, self.y - height//2))
            elif self.piece_type == QUEEN:
                width, height = BLACK_QUEEN.get_rect().size
                win.blit(BLACK_QUEEN, (self.x - width//2, self.y - height//2))
            elif self.piece_type == KING:
                width, height = BLACK_KING.get_rect().size
                win.blit(BLACK_KING, (self.x - width//2, self.y - height//2))
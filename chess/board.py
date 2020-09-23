import pygame
import os
from .constants import ROWS, COLS, SQUARE_SIZE, BROWN, GRAY, WHITE, BLACK, BACK_ROW_ORDER, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, TAKE, MOVE, GUARD, RED, GREEN
from .piece import Piece
from .promotion import Promotion

class Board:
    def __init__(self):
        self.board = []
        self.white_pieces = {PAWN: 8, KNIGHT: 2, BISHOP: 2, ROOK: 2, QUEEN: 1, KING: 1}
        self.black_pieces = {PAWN: 8, KNIGHT: 2, BISHOP: 2, ROOK: 2, QUEEN: 1, KING: 1}
        self.prev_move = (None, -1, -1)
        self._create_board()
    
    def _create_board(self):
        for row in range(ROWS):
            pieces = [0] * COLS

            if row == 0:
                for col in range(COLS):
                    pieces[col] = Piece(row, col, BLACK, BACK_ROW_ORDER[col])
            elif row == 1:
                for col in range(COLS):
                    pieces[col] = Piece(row, col, BLACK, PAWN)
            elif row == 6:
                for col in range(COLS):
                    pieces[col] = Piece(row, col, WHITE, PAWN)
            elif row == 7:
                for col in range(COLS):
                    pieces[col] = Piece(row, col, WHITE, BACK_ROW_ORDER[col])
            
            self.board.append(pieces)
    
    def _draw_squares(self, win, moves):
        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) in moves:
                    if moves[(row, col)] == TAKE:
                        pygame.draw.rect(win, RED, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
                    else:
                        pygame.draw.rect(win, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
                elif (row % 2 == 0 or row % 2 == 1) and col % 2 == row % 2:
                    pygame.draw.rect(win, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def _take_piece(self, selected_piece, piece_taken):
        if piece_taken.colour == WHITE:
            self.white_pieces[piece_taken.piece_type] -= 1
        else:
            self.black_pieces[piece_taken.piece_type] -= 1
    
    def _promote_pawn(self, piece, win):
        promotion_pieces = [QUEEN, ROOK, BISHOP, KNIGHT]
        selection = []
        for i in range(len(promotion_pieces)):
            selection.append(Promotion(promotion_pieces[i], piece.colour, piece.row + (-1 * piece.direction * i), piece.col))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // SQUARE_SIZE
                    col = x // SQUARE_SIZE
                    if col != piece.col or (piece.colour == WHITE and row > 3) or (piece.colour == BLACK and row < 4):
                        break
                    else:
                        diff = abs(row - piece.row)
                        selected_promotion = selection[diff]
                        if piece.colour == WHITE:
                            self.white_pieces[PAWN] -= 1
                            piece.piece_type = selected_promotion.piece_type
                            self.white_pieces[selected_promotion.piece_type] += 1
                        else:
                            self.black_pieces[PAWN] -= 1
                            piece.piece_type = selected_promotion.piece_type
                            self.black_pieces[selected_promotion.piece_type] += 1
                        run = False
            
            # draw promotions
            for s in selection:
                s.draw(win)
            
            pygame.display.update()
    
    def _guarded(self, square, piece):
        row, col = square
        for r in self.board:
            for sq in r:
                if sq != 0 and sq.colour != piece.colour:
                    possible_moves = sq.get_possible_moves(self.board)
                    possible_squares = list(possible_moves.keys())
                    if (sq.piece_type == PAWN and (row, col) in possible_squares and (possible_moves[(row, col)] == TAKE or possible_moves[(row, col)] == GUARD)) or \
                        (sq.piece_type != PAWN and (row, col) in possible_squares and (possible_moves[(row, col)] == GUARD or possible_moves[(row, col)] == MOVE)):
                        return True
        return False
    
    def _en_passant(self, selected, target_sq):
        row, col = target_sq
        if selected.piece_type == PAWN and ((selected.colour == WHITE and selected.row == 3) or (selected.colour == BLACK and selected.row == 4)):
                piece, from_row, from_col = self.prev_move[0], self.prev_move[1], self.prev_move[2]
                if piece.piece_type == PAWN and piece.row + (selected.direction * 2) == from_row:
                    if from_col == col:
                        return True
        return False
    
    def get_viable_moves(self, selected):
        viable_moves = selected.get_possible_moves(self.board)

        if selected.piece_type == KING:
            delete = [key for key in viable_moves if self._guarded((key[0], key[1]), selected) or viable_moves[key] == GUARD]
            for key in delete: del viable_moves[key]
        elif selected.piece_type == PAWN:
            delete = [key for key in viable_moves if viable_moves[key] == GUARD and not self._en_passant(selected, key)]
            for key in delete: del viable_moves[key]

            for move in viable_moves:
                if viable_moves[move] == GUARD:
                    # highlight en passant move as red
                    viable_moves[move] = TAKE
        else:
            delete = [key for key in viable_moves if viable_moves[key] == GUARD]
            for key in delete: del viable_moves[key]

        return viable_moves

    def move(self, piece, row, col, win=None):
        piece_row, piece_col = piece.row, piece.col
        if self.board[row][col] == 0 and not self._en_passant(piece, (row, col)):
            self.board[row][col], self.board[piece_row][piece_col] = self.board[piece_row][piece_col], self.board[row][col]
            piece.move(row, col)

            # check if pawn reached opposite back row
            if piece.piece_type == PAWN and ((row == 0 and piece.colour == WHITE) or (row == 7 and piece.colour == BLACK)):
                # promote pawn
                self._promote_pawn(piece, win)
        else:
            if self._en_passant(piece, (row, col)):
                self._take_piece(piece, self.board[self.prev_move[0].row][self.prev_move[0].col])
                self.board[self.prev_move[0].row][self.prev_move[0].col] = 0
            else:
                self._take_piece(piece, self.board[row][col])
            self.board[piece_row][piece_col] = 0
            piece.move(row, col)
            self.board[row][col] = piece

            # check if pawn reached opposite back row
            if piece.piece_type == PAWN and ((row == 0 and piece.colour == WHITE) or (row == 7 and piece.colour == BLACK)):
                # promote pawn
                self._promote_pawn(piece, win)
        
        self.prev_move = (piece, piece_row, piece_col)
    
    def draw(self, win, moves):
        self._draw_squares(win, moves)
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.draw(win)
    
    def in_check(self, turn):
        # check if the current turn is in check
        for row in self.board:
            for sq in row:
                if sq == 0:
                    continue
                elif sq.colour == turn:
                    continue
                else:
                    moves = self.get_viable_moves(sq)
                    for move in moves:
                        r, c = move
                        if moves[move] == TAKE and self.board[r][c].piece_type == KING:
                            return True
        return False
    
    def check_move(self, selected, dest):
        row, col = dest
        if selected.piece_type == KING and self._guarded(dest, selected):
            # king is trying to move into check - not allowed
            return False
        elif self.in_check(selected.colour) and selected.piece_type != KING:
            # check if the piece can block the check
            selected_sq = self.board[selected.row][selected.col]
            dest_sq = self.board[row][col]
            self.board[selected.row][selected.col] = 0
            self.board[row][col] = selected_sq
            if self.in_check(selected.colour):
                self.board[row][col] = dest_sq
                self.board[selected_sq.row][selected_sq.col] = selected_sq
                return False
            else:
                self.board[row][col] = dest_sq
                self.board[selected_sq.row][selected_sq.col] = selected_sq
                return True
        return True
    
    def castle(self, selected, row, col):
        if selected.col - col > 0:
            # queen's side
            self.move(selected, row, col)
            self.move(self.board[row][col - 2], row, col + 1)
        else:
            # king's side
            self.move(selected, row, col)
            self.move(self.board[row][col + 1], row, col - 1)
    
    def stalemate(self, turn):
        for row in self.board:
            for sq in row:
                if sq != 0 and sq.colour == turn:
                    moves = self.get_viable_moves(sq)
                    if len(moves) != 0:
                        return False
        return True

    def checkmate(self, turn):
        for row in self.board:
            for sq in row:
                if sq != 0 and sq.colour == turn:
                    moves = self.get_viable_moves(sq)
                    for move in moves:
                        if self.check_move(sq, move):
                            return False
        return True
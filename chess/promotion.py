import pygame
from .constants import SQUARE_SIZE, WHITE, BLACK, PAWN, WHITE_PAWN, BLACK_PAWN, KNIGHT, WHITE_KNIGHT, BLACK_KNIGHT, BISHOP, WHITE_BISHOP, BLACK_BISHOP, ROOK, WHITE_ROOK, BLACK_ROOK, \
    QUEEN, WHITE_QUEEN, BLACK_QUEEN, KING, WHITE_KING, BLACK_KING, DARK_GRAY

class Promotion:
    def __init__(self, piece_type, colour, row, col):
        self.piece_type = piece_type
        self.colour = colour
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self._calc_pos()
        self.width = self.height = SQUARE_SIZE
    
    def _calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw(self, win):
        pygame.draw.rect(win, DARK_GRAY, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, BLACK, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
        if self.colour == WHITE:
            if self.piece_type == KNIGHT:
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
        else:
            if self.piece_type == KNIGHT:
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
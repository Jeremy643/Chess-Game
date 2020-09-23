import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
BOARD_WIDTH, BOARD_HEIGHT = 800, 800
ROWS = COLS = 8
SQUARE_SIZE = BOARD_WIDTH // COLS

# square colours
GRAY = (224, 224, 224)
BROWN = (153, 76, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (105, 105, 105)

# piece colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# chess pieces
PAWN = 'pawn'
KNIGHT = 'knight'
BISHOP = 'bishop'
ROOK = 'rook'
QUEEN = 'queen'
KING = 'king'

# move type
MOVE = 'move'
TAKE = 'take'
GUARD = 'guard'
CASTLE = 'castle'

# back row order
BACK_ROW_ORDER = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]

# chess piece images
WHITE_PAWN = pygame.transform.scale(pygame.image.load('assets/white_pawn.png'), (70, 90))
BLACK_PAWN = pygame.transform.scale(pygame.image.load('assets/black_pawn.png'), (70, 90))
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load('assets/white_knight.png'), (70, 90))
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load('assets/black_knight.png'), (70, 90))
WHITE_BISHOP = pygame.transform.scale(pygame.image.load('assets/white_bishop.png'), (70, 90))
BLACK_BISHOP = pygame.transform.scale(pygame.image.load('assets/black_bishop.png'), (70, 90))
WHITE_ROOK = pygame.transform.scale(pygame.image.load('assets/white_rook.png'), (70, 90))
BLACK_ROOK = pygame.transform.scale(pygame.image.load('assets/black_rook.png'), (70, 90))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load('assets/white_queen.png'), (70, 90))
BLACK_QUEEN = pygame.transform.scale(pygame.image.load('assets/black_queen.png'), (70, 90))
WHITE_KING = pygame.transform.scale(pygame.image.load('assets/white_king.png'), (70, 90))
BLACK_KING = pygame.transform.scale(pygame.image.load('assets/black_king.png'), (70, 90))
import pygame
import os
from chess.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, SQUARE_SIZE, WHITE, BLACK
from chess.game import Game

FPS = 60

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (100, 100)
WIN = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption('Chess')


def get_mouse_row_col(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.stalemate():
            print('Stalemate!\nWhite - 1/2 | Black - 1/2\nGame over.')
            run = False
        elif game.checkmate():
            winner = 'White'
            if game.turn == WHITE:
                winner = 'Black'
            print(f'Checkmate!\n{winner} wins!\nGame over.')
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_row_col(pos)
                game.select(row, col)
        
        game.update()
    
    pygame.quit()

main()
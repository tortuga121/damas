# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from damas.constantes import LARGURA, ALTURA, CASA_SIZE, VERMELHO
from damas.jogo import Jogo

FPS = 60

WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // CASA_SIZE
    col = x // CASA_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Jogo(WIN)

    while run:
        clock.tick(FPS)

        if game.vencedor() != None:
            print(game.vencedor())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.seleciona(row, col)

        game.atualiza()
    
    pygame.quit()

main()
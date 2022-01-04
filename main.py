# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from damas.constantes import LARGURA, ALTURA, CASA_SIZE
from damas.jogo import Jogo

FPS = 60

WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Checkers')

def get_lin_col_rato(pos):
    x, y = pos
    lin = y // CASA_SIZE
    col = x // CASA_SIZE
    return lin, col

def main():
    run = True
    clock = pygame.time.Clock()
    jogo = Jogo(WIN)

    while run:
        clock.tick(FPS)

        if jogo.vencedor() is not None:
            print(jogo.vencedor())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                lin, col = get_lin_col_rato(pos)
                jogo.seleciona(lin, col)

        jogo.atualiza()
    
    pygame.quit()

main()
from .constantes import CASA_SIZE, CINZA, COROA
import pygame


class Peca:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, lin, col, cor):
        ## coordenadads no jgoo
        self.lin = lin
        self.col = col
        self.cor = cor
        self.rei = False
        ## coordenadas na jenal
        self.x = 0
        self.y = 0
        self.calc_pos()

    # passa de coordenadas do jogo para coordenadas da janela
    def calc_pos(self):
        self.x = CASA_SIZE * self.col + CASA_SIZE // 2
        self.y = CASA_SIZE * self.lin + CASA_SIZE // 2

    def faz_rei(self):
        self.rei = True

    def desenha(self, win):
        radius = CASA_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, CINZA, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.cor, (self.x, self.y), radius)
        if self.rei:
            win.blit(COROA, (self.x - COROA.get_width() // 2, self.y - COROA.get_height() // 2))

    def move(self, row, col):
        self.lin = row
        self.col = col
        self.calc_pos()

from .constantes import CASA_SIZE, CINZA, COROA
import pygame


class Peca:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, lin, col, cor):
        """
        Construtor da classe peca
        @param lin: Linha da peca
        @param col: Coluna da peca
        @param cor: cor da peca
        """
        self.lin = lin
        self.col = col
        self.cor = cor
        self.rei = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """
        Preenche os campos x e y com a posicao da peca na janela
        @param self: A peca em si
        """
        self.x = CASA_SIZE * self.col + CASA_SIZE // 2
        self.y = CASA_SIZE * self.lin + CASA_SIZE // 2

    def faz_rei(self):
        """
        Torna a peca num rei
        @param self: Peca em si
        """
        self.rei = True

    def desenha(self, win):
        """
        Desenha a peca na janela
        @param self: A peca em si
        @param win: Janela do jogo
        """
        radius = CASA_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, CINZA, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.cor, (self.x, self.y), radius)
        if self.rei:
            win.blit(COROA, (self.x - COROA.get_width() // 2, self.y - COROA.get_height() // 2))

    def move(self, lin, col):
        """
        Move a Peca alterando a sua linha e coluna
        @param lin: Linha para onde se vai mover
        @param col: Coluna para onde se vai mover
        """
        self.lin = lin
        self.col = col
        self.calc_pos()

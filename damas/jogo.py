import pygame
from damas.constantes import VERMELHO, BRANCO, AZUL, CASA_SIZE
from damas.tabuleiro import Tabuleiro


class Jogo:
    # janela - win
    # quadrado selecionado - selecionado
    # quem é a jogar - vez
    # lista de coordeandas das jogadas validas = jogadas_validas
    # tabuleiro
    def __init__(self, win):
        self._init()
        self.win = win

    def atualiza(self):
        self.tabuleiro.desenha(self.win)
        self.desenha_jogadas_validas(self.jogadas_validas)
        pygame.display.update()

    def _init(self):
        self.selecionado = None
        self.tabuleiro = Tabuleiro()
        self.vez = VERMELHO
        self.jogadas_validas = {}

    def vencedor(self):
        return self.tabuleiro.vencedor()

    def reinicia(self):
        self._init()

    def seleciona(self, lin, col):
        if self.selecionado:
            resultado = self.move(lin, col)
            if not resultado:
                self.selecionado = None
                self.seleciona(lin, col)

        peca = self.tabuleiro.get_peca(lin, col)
        if peca != 0 and peca.cor == self.vez:
            self.selecionado = peca
            self.jogadas_validas = self.tabuleiro.get_jogadas_validas(peca)


    def move(self, lin, col):
        peca = self.tabuleiro.get_peca(lin, col)
        if self.selecionado and peca == 0 and (lin, col) in self.jogadas_validas:
            self.tabuleiro.move(self.selecionado, lin, col)
            removidos = self.jogadas_validas[(lin, col)]
            if removidos:
                self.tabuleiro.remove(removidos)
            self.passa_vez()
        else:
            return False

        return True

    def desenha_jogadas_validas(self, movimentos):
        for mov in movimentos:
            lin, col = mov
            pygame.draw.circle(self.win, AZUL,
                               (col * CASA_SIZE + CASA_SIZE // 2, lin * CASA_SIZE + CASA_SIZE // 2), 15)

    def passa_vez(self):
        self.jogadas_validas = {}
        if self.vez == VERMELHO:
            self.vez = BRANCO
        else:
            self.vez = VERMELHO

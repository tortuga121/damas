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
    # atualiza a jnaela e desenha as coisas do tabuleiro
    def atualiza(self):
        self.tabuleiro.desenha(self.win)
        self.desenha_jogadas_validas(self.jogadas_validas)
        pygame.display.update()

    def _init(self):
        self.selecionado = None
        self.tabuleiro = Tabuleiro()
        self.vez = VERMELHO
        self.jogadas_validas = {}

    # devolve None se não ha vencedor ou uma frase a dizer quem é o vencedor
    def vencedor(self):
        return self.tabuleiro.vencedor()
    # reeinicia o tabuleiro
    def reinicia(self):
        self._init()
    # seleciona um casa do tabuleiro
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

    # move uma peça do tabuleiro se a jogada for valida devolve true se for invalida devolve false
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
    # desenha na janela as jogadas validas com pontos azuis
    def desenha_jogadas_validas(self, movimentos):
        for mov in movimentos:
            lin, col = mov
            pygame.draw.circle(self.win, AZUL,
                               (col * CASA_SIZE + CASA_SIZE // 2, lin * CASA_SIZE + CASA_SIZE // 2), 15)
    # troca a vez de quem é o proximo a jogar
    def passa_vez(self):
        self.jogadas_validas = {}
        if self.vez == VERMELHO:
            self.vez = BRANCO
        else:
            self.vez = VERMELHO

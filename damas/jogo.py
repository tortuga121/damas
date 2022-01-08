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
        """
        Comstrutor da classe jogo
        @param win: Janela do joogo
        """
        self._init()
        self.win = win
    # atualiza a jnaela e desenha as coisas do tabuleiro
    def atualiza(self):
        self.tabuleiro.desenha(self.win)
        self.desenha_jogadas_validas(self.jogadas_validas)
        pygame.display.update()

    def _init(self):
        """
        Metodo auxiliar do construtor
        """
        self.selecionado = None
        self.tabuleiro = Tabuleiro()
        self.vez = VERMELHO
        self.jogadas_validas = {}

    def vencedor(self):
        """
        Calcula qual é o vencedor
        @return: String que diz quem é o vencedor
        """
        return self.tabuleiro.vencedor()

    def reinicia(self):
        """
        Reeinicia o tabuleiro para o inicio do jogo
        """
        self._init()

    def seleciona(self, lin, col):
        """
        Seleciona um quadrado do tabuleiro
        @param lin: Linha do quadrado selecionado
        @param col: Coluna do quadrado selecionado
        """
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
        """
        Move uma peca do jogo
        @param lin: Linha de onde se encontra a peca
        @param col: Coluna de onde se encontra a peca
        @return: Boolean que é verdadeiro caso alguma peca se tenha movido
         falso caso o mesmo nao tenha acontecido
        """
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
        """
        Desenha na janela as jogadas validas com pontos azuis
        @param movimentos: Um dicionario com os movimentos possiveis
        """
        for mov in movimentos:
            lin, col = mov
            pygame.draw.circle(self.win, AZUL,
                               (col * CASA_SIZE + CASA_SIZE // 2, lin * CASA_SIZE + CASA_SIZE // 2), 15)

    def passa_vez(self):
        """
        Alterna a vez do jogador
        """
        self.jogadas_validas = {}
        if self.vez == VERMELHO:
            self.vez = BRANCO
        else:
            self.vez = VERMELHO

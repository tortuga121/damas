import pygame
from .constantes import VERMELHO, BRANCO, AZUL, CASA_SIZE
from damas.tabuleiro import Tabuleiro


class Jogo:
    def __init__(self, win):
        self._init()
        self.win = win

    def atualiza(self):
        self.board.desenha(self.win)
        self.desenha_jogadas_validas(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Tabuleiro()
        self.turn = VERMELHO
        self.valid_moves = {}

    def vencedor(self):
        return self.board.vencedor()

    def reinicia(self):
        self._init()

    def seleciona(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.seleciona(row, col)

        piece = self.board.get_peca(row, col)
        if piece != 0 and piece.cor == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_jogadas_validas(piece)
            return True

        return False

    def move(self, row, col):
        piece = self.board.get_peca(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.passa_vez()
        else:
            return False

        return True

    def desenha_jogadas_validas(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, AZUL,
                               (col * CASA_SIZE + CASA_SIZE // 2, row * CASA_SIZE + CASA_SIZE // 2), 15)

    def passa_vez(self):
        self.valid_moves = {}
        if self.turn == VERMELHO:
            self.turn = BRANCO
        else:
            self.turn = VERMELHO

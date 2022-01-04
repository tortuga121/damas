import pygame
from .constantes import PRETO, FILAS, VERMELHO, CASA_SIZE, COLUNAS, BRANCO, CASTANHO
from .pecas import Peca


class Tabuleiro:
    def __init__(self):
        self.tab = []
        self.pecas_vermelhas = self.pecas_brancas = 12
        self.reis_vermelhos = self.reis_brancos = 0
        self.cria_tabuleiro()

    def desenha_quadrados(self, win):
        win.fill(PRETO)
        for lin in range(FILAS):
            for col in range(lin % 2, COLUNAS, 2):
                pygame.draw.rect(win, CASTANHO, (lin * CASA_SIZE, col * CASA_SIZE, CASA_SIZE, CASA_SIZE))

    def move(self, peca, row, col):
        self.tab[peca.fila][peca.col], self.tab[row][col] = self.tab[row][col], self.tab[peca.fila][peca.col]
        peca.move(row, col)

        if row == FILAS - 1 or row == 0:
            peca.faz_rei()
            if peca.cor == BRANCO:
                self.reis_brancos += 1
            else:
                self.reis_vermelhos += 1

    def get_peca(self, row, col):
        return self.tab[row][col]

    def cria_tabuleiro(self):
        for lin in range(FILAS):
            self.tab.append([])
            for col in range(COLUNAS):
                if col % 2 == ((lin + 1) % 2):
                    if lin < 3:
                        self.tab[lin].append(Peca(lin, col, BRANCO))
                    elif lin > 4:
                        self.tab[lin].append(Peca(lin, col, VERMELHO))
                    else:
                        self.tab[lin].append(0)
                else:
                    self.tab[lin].append(0)

    def desenha(self, win):
        self.desenha_quadrados(win)
        for lin in range(FILAS):
            for col in range(COLUNAS):
                piece = self.tab[lin][col]
                if piece != 0:
                    piece.desenha(win)

    def remove(self, pecas):
        for peca in pecas:
            self.tab[peca.fila][peca.col] = 0
            if peca != 0:
                if peca.cor == VERMELHO:
                    self.pecas_vermelhas -= 1
                else:
                    self.pecas_brancas -= 1

    def vencedor(self):
        if self.pecas_vermelhas <= 0:
            return BRANCO
        elif self.pecas_brancas <= 0:
            return VERMELHO

        return None

    def get_jogadas_validas(self, piece):
        movimentos = {}
        esq = piece.col - 1
        dir = piece.col + 1
        lin = piece.fila

        if piece.cor == VERMELHO or piece.rei:
            movimentos.update(self.diagonal_esq(lin - 1, max(lin - 3, -1), -1, piece.cor, esq, []))
            movimentos.update(self.diagonal_dir(lin - 1, max(lin - 3, -1), -1, piece.cor, dir, []))
        if piece.cor == BRANCO or piece.rei:
            movimentos.update(self.diagonal_esq(lin + 1, min(lin + 3, FILAS), 1, piece.cor, esq, []))
            movimentos.update(self.diagonal_dir(lin + 1, min(lin + 3, FILAS), 1, piece.cor, dir, []))

        return movimentos

    def diagonal_esq(self, start, stop, step, color, left, saltados):
        movimentos = {}
        ultimo = []
        for r in range(start, stop, step):
            if left < 0:
                break

            atual = self.tab[r][left]
            if atual == 0:
                if saltados and not ultimo:
                    break
                elif saltados:
                    movimentos[(r, left)] = ultimo + saltados
                else:
                    movimentos[(r, left)] = ultimo

                if ultimo:
                    if step == -1:
                        lin = max(r - 3, 0)
                    else:
                        lin = min(r + 3, FILAS)
                    movimentos.update(self.diagonal_esq(r + step, lin, step, color, left - 1, ultimo))
                    movimentos.update(self.diagonal_dir(r + step, lin, step, color, left + 1, ultimo))
                break
            elif atual.cor == color:
                break
            else:
                ultimo = [atual]

            left -= 1

        return movimentos

    def diagonal_dir(self, start, stop, step, cor, right, saltados):
        movimentos = {}
        ultimo = []
        for r in range(start, stop, step):
            if right >= COLUNAS:
                break

            atual = self.tab[r][right]
            if atual == 0:
                if saltados and not ultimo:
                    break
                elif saltados:
                    movimentos[(r, right)] = ultimo + saltados
                else:
                    movimentos[(r, right)] = ultimo

                if ultimo:
                    if step == -1:
                        lin = max(r - 3, 0)
                    else:
                        lin = min(r + 3, FILAS)
                    movimentos.update(self.diagonal_esq(r + step, lin, step, cor, right - 1, ultimo))
                    movimentos.update(self.diagonal_dir(r + step, lin, step, cor, right + 1, ultimo))
                break
            elif atual.cor == cor:
                break
            else:
                ultimo = [atual]

            right += 1

        return movimentos

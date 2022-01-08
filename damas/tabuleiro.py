import pygame
from .constantes import PRETO, FILAS, VERMELHO, CASA_SIZE, COLUNAS, BRANCO, CASTANHO
from .pecas import Peca


class Tabuleiro:

    def __init__(self):
        """
        Construtor da classe Tabuleiro
        """
        self.tab = []
        self.pecas_vermelhas = 12
        self.pecas_brancas = 12
        self.reis_vermelhos = 0
        self.reis_brancos = 0
        self.cria_tabuleiro()

    def desenha_quadrados(self, win):
        """
        Desenha os quadrados na janela do jogo
        @param win: Janela de jogo
        """
        win.fill(PRETO)
        for lin in range(FILAS):
            for col in range(lin % 2, COLUNAS, 2):
                pygame.draw.rect(win, CASTANHO, (lin * CASA_SIZE, col * CASA_SIZE, CASA_SIZE, CASA_SIZE))

    def move(self, peca, lin, col):
        """
        Move uma peca do tabuleiro
        @param peca: Peca que vai ser movida
        @param lin: Linha para onde a peca vai
        @param col: Coluna para onde a peca vai
        """
        self.tab[peca.lin][peca.col], self.tab[lin][col] = self.tab[lin][col], self.tab[peca.lin][peca.col]
        peca.move(lin, col)

        if lin == FILAS - 1 or lin == 0:
            peca.faz_rei()
            if peca.cor == BRANCO:
                self.reis_brancos += 1
            else:
                self.reis_vermelhos += 1

    def get_peca(self, lin, col):
        """
        Obtem a peca que se encontra na posicao dada nos parametros
        @param lin: Linha da peca
        @param col: Coluna da Peca
        @return: Peca que se encontra na posicao dada
        """
        return self.tab[lin][col]

    def cria_tabuleiro(self):
        """
        Preenche o matriz do tabueliro (tab)
        como se fosse o inicio do jogo
        """
        for lin in range(FILAS):
            self.tab.append([])
            for col in range(COLUNAS):
                # se um for par e o outro impar vamos colocar peca
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
        """
        Desenha na janelao tabueleiro e as suas pecas
        @param win: janela do jogo
        """
        self.desenha_quadrados(win)
        for lin in range(FILAS):
            for col in range(COLUNAS):
                piece = self.tab[lin][col]
                if piece != 0:
                    piece.desenha(win)

    def remove(self, pecas):
        """
        Remove uma ou mais pecas do tabueliro substituindo as por 0
        @param pecas: Lista de pecas a remover
        """
        for peca in pecas:
            self.tab[peca.lin][peca.col] = 0
            if peca != 0:
                if peca.cor == VERMELHO:
                    self.pecas_vermelhas -= 1
                else:
                    self.pecas_brancas -= 1

    def vencedor(self):
        """
        determina quem é o vencedor a partir do nuemro
        de pecas no tabueliro de cada cor
        @return: String que indica quem é o vencedor
        """
        if self.pecas_vermelhas <= 0:
            return "GANHARAM AS PECAS BRANCAS"
        elif self.pecas_brancas <= 0:
            return "GANHARAM AS PECAS VERMELHAS"

        return None

    def get_jogadas_validas(self, peca):
        """
        Obtem as jogadas possiveis para uma determinada peca
        na forma de um dicionario contendo tambem as pecas que saltou
        @param peca: A peca em questao
        """
        movimentos = {}
        esq = peca.col - 1
        direita = peca.col + 1
        lin = peca.lin

        if peca.cor == VERMELHO or peca.rei:
            movimentos.update(self.diagonal_esq(lin - 1, max(lin - 3, -1), -1, peca.cor, esq))
            movimentos.update(self.diagonal_dir(lin - 1, max(lin - 3, -1), -1, peca.cor, direita))
        if peca.cor == BRANCO or peca.rei:
            movimentos.update(self.diagonal_esq(lin + 1, min(lin + 3, FILAS), 1, peca.cor, esq))
            movimentos.update(self.diagonal_dir(lin + 1, min(lin + 3, FILAS), 1, peca.cor, direita))

        return movimentos

    def diagonal_esq(self, start, stop, step, color, left, saltados=[]):
        """
        Calcula as jogadas possiveis na diagonal esquerda
        @param start: Linha em que começa
        @param stop: Linha onde para
        @param step: Pode ser 1 ou -1 dependendo se são vermelhas brancas ou o rei
        @param color: Cor da peca em questao
        @param left: coluna para onde se pode mover
        @param saltados: Lista das pecas saltadas
        @return: Jogadas possiveis na diagonal da esquerda
        """
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
                    movimentos.update(self.diagonal_esq(r + step, lin, step, color, left - 1, saltados=ultimo))
                    movimentos.update(self.diagonal_dir(r + step, lin, step, color, left + 1, saltados=ultimo))
                break
            elif atual.cor == color:
                break
            else:
                ultimo = [atual]

            left -= 1

        return movimentos

    def diagonal_dir(self, start, stop, step, cor, right, saltados=[]):
        """
        Calcula as jogadas possiveis na diagonal direita
        @param start: Linha em que começa
        @param stop: Linha onde para
        @param step: Pode ser 1 ou -1 dependendo se são vermelhas brancas ou o rei
        @param cor: Cor da peca em questao
        @param right: coluna para onde se pode mover
        @param saltados: Lista das pecas saltadas
        @return: Jogadas possiveis na diagonal da direita
        """
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
                    movimentos.update(self.diagonal_esq(r + step, lin, step, cor, right - 1, saltados=ultimo))
                    movimentos.update(self.diagonal_dir(r + step, lin, step, cor, right + 1, saltados=ultimo))
                break
            elif atual.cor == cor:
                break
            else:
                ultimo = [atual]

            right += 1

        return movimentos

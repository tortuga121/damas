import pygame

LARGURA, ALTURA = 800, 800
FILAS, COLUNAS = 8, 8
CASA_SIZE = LARGURA // COLUNAS

# rgb
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
CINZA = (128, 128, 128)
CASTANHO = (102,51,0)

COROA = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

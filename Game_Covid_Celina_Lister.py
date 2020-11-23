import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
JANELA = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kill Covid Game")

# Load images
INIMIGO_VERMELHO = pygame.image.load(os.path.join("covid_vermelho.png"))
INIMIGO_VERDE = pygame.image.load(os.path.join("covid_verde.png"))
INIMIGO_AZUL = pygame.image.load(os.path.join("covid_azul.png"))

# Player player #NAVE DO JOGADOR
logo_sus = pygame.image.load(os.path.join("logo_sus.png"))

# Lasers
CORONA_VERMELHO = pygame.image.load(os.path.join("laser_vermelho.png"))
CORONA_VERDE = pygame.image.load(os.path.join("laser_verde.png"))
CORONA_AZUL = pygame.image.load(os.path.join("laser_azul.png"))
VACINA = pygame.image.load(os.path.join("vacina_covid.png"))

#Fundo do jogo
FUNDO_COVID= pygame.transform.scale(pygame.image.load(os.path.join("fundo_covid.png")), (WIDTH, HEIGHT))

class Corona:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def desenhar(self, janelinha):
        janelinha.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def fora_da_tela(self, height):
        return not(self.y <= height and self.y >= 0)

    def impacto(self, obj):
        return collide(self, obj)

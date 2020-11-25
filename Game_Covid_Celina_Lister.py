#Jogo criado utilizando a Biblioteca Pygame
#A ideia do jogo é "matar o covid", onde o logotipo do SUS lança vacinas no vírus.

#Foi criado um novo repositório, pois o anterior estava com as imagens excessivamente grandes,
#assim como discutimos anteriormente com o professor durante a aula.

#Integrantes do grupo:
#Celina Melo e Lister Ogusuku

#Design de Software | Insper 2020.2

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#Importando as bibliotecas necessárias
import pygame
import os
import time
import random

pygame.font.init() #Fonte para ser utilizada no jogo

#Definindo altura e largura da janela do jogo
WIDTH, HEIGHT = 750, 750 #Dimensões do display
JANELA = pygame.display.set_mode((WIDTH, HEIGHT)) #Definição do display
pygame.display.set_caption("Kill Covid Game") #Nome do jogo

#Imagens que vão ser utilizadas
INIMIGO_VERMELHO = pygame.image.load(os.path.join("covid_vermelho.png")) #Covid vermelho
INIMIGO_VERDE = pygame.image.load(os.path.join("covid_verde.png")) #Covid verde
INIMIGO_AZUL = pygame.image.load(os.path.join("covid_azul.png")) #Covid azul

#NAVE DO JOGADOR
logo_sus = pygame.image.load(os.path.join("logo_sus.png")) #Nave do jogador feita com o logotipo do SUS

# Lasers
CORONA_VERMELHO = pygame.image.load(os.path.join("laser_vermelho.png")) #laser que o covid lança #se quiser, pode pensar em mais coisas além do laser, mas temos pouco tempo
CORONA_VERDE = pygame.image.load(os.path.join("laser_verde.png")) #laser que o covid lança
CORONA_AZUL = pygame.image.load(os.path.join("laser_azul.png")) #laser que o covid lança
VACINA = pygame.image.load(os.path.join("vacina_covid.png")) #laser que o covid lança

#Fundo do jogo
FUNDO_COVID= pygame.transform.scale(pygame.image.load(os.path.join("fundo_covid.png")), (WIDTH, HEIGHT))

class Corona:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
#Desenhando a janela do jogo
    def desenhar(self, janelinha):
        janelinha.blit(self.img, (self.x, self.y))
#Definindo os movimentos
    def move(self, vel):
        self.y += vel

    def fora_da_tela(self, height):
        return not(self.y <= height and self.y >= 0)

    def impacto(self, obj):
        return colide(self, obj)

class Nave:
    Tempo_de_espera = 30

    def __init__(self, x, y, health=100):  #O que é esse health? Não entendi
        self.x = x
        self.y = y
        self.health = health
        self.nave_img = None
        self.laser_img = None
        self.lasers = []
        self.contador_tempo_espera = 0

    def desenhar(self, janelinha):
        janelinha.blit(self.nave_img, (self.x, self.y))
        for laser in self.lasers:
            laser.desenhar(janelinha)

    def move_lasers(self, vel, obj):
        self.tempo_espera()
        for laser in self.lasers:
            laser.move(vel)
            if laser.fora_da_tela(HEIGHT):
                self.lasers.remove(laser)
            elif laser.impacto(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def tempo_espera(self): #Define tempo de espera
        if self.contador_tempo_espera >= self.Tempo_de_espera:
            self.contador_tempo_espera = 0
        elif self.contador_tempo_espera > 0:
            self.contador_tempo_espera += 1

    def atirar(self): #Função designada para atirar
        if self.contador_tempo_espera == 0:
            laser = Corona(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.contador_tempo_espera = 1

    def get_width(self):
        return self.nave_img.get_width()

    def get_height(self):
        return self.nave_img.get_height()

class Jogador(Nave): #Nave do Jogador (SUS)
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.nave_img = logo_sus
        self.laser_img = VACINA
        self.mask = pygame.mask.from_surface(self.nave_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.tempo_espera()
        for laser in self.lasers:
            laser.move(vel)
            if laser.fora_da_tela(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.impacto(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def desenhar(self, janelinha):
        super().desenhar(janelinha)
        self.barra_de_vidas(janelinha)

    def barra_de_vidas(self, janelinha): #Vida disponível
        pygame.draw.rect(janelinha, (255,0,0), (self.x, self.y + self.nave_img.get_height() + 10, self.nave_img.get_width(), 10))
        pygame.draw.rect(janelinha, (0,255,0), (self.x, self.y + self.nave_img.get_height() + 10, self.nave_img.get_width() * (self.health/self.max_health), 10))


class Inimigo(Nave): #Nave Inimiga (Corona)
    COR_MAP = {
                "vermelho": (INIMIGO_VERMELHO, CORONA_VERMELHO),
                "verde": (INIMIGO_VERDE, CORONA_VERDE),
                "azul": (INIMIGO_AZUL, CORONA_AZUL)
                }

    def __init__(self, x, y, cor, health=100):
        super().__init__(x, y, health)
        self.nave_img, self.laser_img = self.COR_MAP[cor]
        self.mask = pygame.mask.from_surface(self.nave_img)

    def move(self, vel):
        self.y += vel

    def atirar(self):
        if self.contador_tempo_espera == 0:
            laser = Corona(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.contador_tempo_espera = 1


def colide(obj1, obj2): #Define a colisão dos objetos
    desloc_x = obj2.x - obj1.x #Deslocamento em x
    desloc_y = obj2.y - obj1.y #Deslocamento em y
    return obj1.mask.overlap(obj2.mask, (desloc_x, desloc_y)) != None  #retorna objetos

def principal():
    anda = True
    FPS = 60
    fase = 0
    vidas = 5
    texto_inicio = pygame.font.SysFont("Century Ghotic", 50)
    texto_quando_perde = pygame.font.SysFont("Century Ghotic", 60)

    inimigos = []
    alcance_do_inimigo = 5
    velocidade_do_inimigo = 1

    velocidade_do_jogador = 5
    velocidade_do_laser = 5

    jogador = Jogador(300, 630)

    temporizador = pygame.time.Clock()

    perdeu = False
    contador_perdeu = 0

#Escrita na tela das vidas e fases

    def desenhar_janela():
        JANELA.blit(FUNDO_COVID, (0,0))
        vidas_label = texto_inicio.render(f"Vidas: {vidas}", 1, (255,255,255))
        fase_label = texto_inicio.render(f"Fase: {fase}", 1, (255,255,255))

        JANELA.blit(vidas_label, (10, 10))
        JANELA.blit(fase_label, (WIDTH - fase_label.get_width() - 10, 10))

        for inimigo in inimigos:
            inimigo.desenhar(JANELA)

        jogador.desenhar(JANELA)

        if perdeu:
            texto_perdeu = texto_quando_perde.render("Você foi contaminado!!", 1, (255,255, 255))
            JANELA.blit(texto_perdeu, (WIDTH/2 - texto_perdeu.get_width()/2, 350))

        pygame.display.update()

    while anda:
        temporizador.tick(FPS)
        desenhar_janela()

        if vidas <= 0 or jogador.health <= 0:
            perdeu = True
            contador_perdeu += 1

        if perdeu:
            if contador_perdeu > FPS * 3:
                anda = False
            else:
                continue

        if len(inimigos) == 0:
            fase += 1
            alcance_do_inimigo += 5
            for i in range(alcance_do_inimigo):
                inimigo = Inimigo(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["vermelho", "azul", "verde"]))
                inimigos.append(inimigo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and jogador.x - velocidade_do_jogador > 0: #Setinha da esquerda
            jogador.x -= velocidade_do_jogador
        if keys[pygame.K_d] and jogador.x + velocidade_do_jogador + jogador.get_width() < WIDTH: #Setinha da direita
            jogador.x += velocidade_do_jogador
        if keys[pygame.K_w] and jogador.y - velocidade_do_jogador > 0: #Setinha pra cima
            jogador.y -= velocidade_do_jogador
        if keys[pygame.K_s] and jogador.y + velocidade_do_jogador + jogador.get_height() + 15 < HEIGHT: #Setinha pra baixo
            jogador.y += velocidade_do_jogador
        if keys[pygame.K_SPACE]: #Espaço para atirar
            jogador.atirar()

        for inimigo in inimigos[:]: #Movimento do covid
            inimigo.move(velocidade_do_inimigo)
            inimigo.move_lasers(velocidade_do_laser, jogador)

            if random.randrange(0, 2*60) == 1:
                inimigo.atirar() #tiro de vírus do covid com laser

            if colide(inimigo, jogador):
                jogador.health -= 10
                inimigos.remove(inimigo)
            elif inimigo.y + inimigo.get_height() > HEIGHT:
                vidas -= 1
                inimigos.remove(inimigo)

        jogador.move_lasers(-velocidade_do_laser, inimigos)

def tela_principal():
    fonte_titulo = pygame.font.SysFont("Century Ghotic", 70)
    anda = True
    while anda:
        JANELA.blit(FUNDO_COVID, (0,0))
        title_label = fonte_titulo.render("Clique para começar", 1, (255,255,255))
        JANELA.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                anda = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                principal()
    pygame.quit()


tela_principal()

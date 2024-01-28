import pygame as pg
import sys
import random as rd

# Konstanter
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTYELLOW = (253, 250, 114)
BABYBLUE = (137, 207, 240)

# Klasser
class Spillobjekt:
    def __init__(self, xPosisjon, yPosisjon):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon

    def plassering(self):
        self.xPosisjon = rd.randint(100, WIDTH - 200)
        self.yPosisjon = rd.randint(0, HEIGHT - 25)

class Menneske(Spillobjekt):
    def __init__(self, fart, poeng, bærerSau):
        super().__init__(0, 0)
        self.fart = fart
        self.poeng = poeng
        self.bærerSau = bærerSau

    def plassering(self):
        self.xPosisjon = rd.randint(0, 100 - 25)
        self.yPosisjon = rd.randint(0, HEIGHT - 25)

    def beveg(self):
        keys = pg.key.get_pressed()
        self.retning_x = 0
        self.retning_y = 0

        if keys[pg.K_LEFT] and self.xPosisjon >= 0:
            self.retning_x = -5
        if keys[pg.K_RIGHT] and self.xPosisjon <= WIDTH - W + 1:
            self.retning_x = 5
        if keys[pg.K_DOWN] and self.yPosisjon <= HEIGHT - H + 1:
            self.retning_y = 5
        if keys[pg.K_UP] and self.yPosisjon >= 0:
            self.retning_y = -5

        self.xPosisjon += self.retning_x
        self.yPosisjon += self.retning_y

class Spøkelse(Spillobjekt):
    def __init__(self):
        super().__init__(0, 0)
        self.vx = 3
        self.vy = 3

    def tegnSpøkelse(self):
        pg.draw.rect(surface, BLUE, [self.xPosisjon, self.yPosisjon, 25, 25])

# Initierer pygame
pg.init()

# Lager en overflate vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjøres
run = True

# Oppretter menneskeobjektet
menneske = Menneske(0, 0, False)
menneske.plassering()
W = 25
H = 25

# Oppretter spøkelseobjekter
spøkelse1 = Spøkelse()
spøkelse1.plassering()

# Spill-løkken
while run:
    # Sørger for at løkken kjøres i korrekt hastighet
    clock.tick(FPS)

    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False  # Spillet skal avsluttes

    # Kaller menneske bevegmetoden
    menneske.beveg()

    # Fyller skjermen med en farge
    surface.fill(WHITE)
    pg.draw.rect(surface, LIGHTYELLOW, [0, 0, 100, HEIGHT])
    pg.draw.rect(surface, LIGHTYELLOW, [WIDTH - 100, 0, 100, HEIGHT])
    pg.draw.rect(surface, BABYBLUE, [100, 0, WIDTH - 200, HEIGHT])

    # Tegner Menneske
    pg.draw.rect(surface, RED, [menneske.xPosisjon, menneske.yPosisjon, W, H])

    # Tegner spøkelsene
    spøkelse1.tegnSpøkelse()

    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()

# Avslutter pygame
pg.quit()
sys.exit()

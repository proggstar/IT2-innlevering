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
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initierer pygame
pg.init()

# Lager en overflate vi kan tegne pa
surface = pg.display.set_mode(SIZE)

# Lager klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjores
run = True

# Klasser
class Spillbrett:
    spokelser = [] # Liste av Spøkelse. List<Spøkelse>
    hindringer = [] # Liste av Hindring. List<Hindring>
    sauer = [] # Liste av Sau. 

    def leggTilSpillObjekt(self,spillobjekt): 
        if isinstance(spillobjekt, Spokelse):
            self.spokelser.append(spillobjekt)
            print("Jeg la til Spokelse")
        
        elif isinstance(spillobjekt, Hindring):
            self.hindringer.append(spillobjekt)
            print("Jeg la til Hindring")

        else:
            self.sauer.append(spillobjekt)
            print("Jeg la til Sau")

        


    def fjernSpillObjekt(self, spillobjekt):
        if isinstance(spillobjekt, Spokelse):
            spokelse.pop(spillobjekt)
        
        elif isinstance(spillobjekt, Hindring):
            hindringer.pop(spillobjekt)

        else:
            sau.pop(spillobjekt)
        
        print("Jeg fjernet et ", + spillobjekt)


class Spillobjekt:
    def __init__(self, xPosisjon, yPosisjon):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon

    def plassering(self):
        self.xPosisjon = 0
        self.yPosisjon = 0

    def hentPosisjon(self):
        return (self.xPosisjon, self.yPosisjon)


class Spokelse(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(100, WIDTH - 200), rd.randint(0, HEIGHT - 25))
        self.vx = 3
        self.vy = 3

    def tegnSpokelse(self):
        pg.draw.rect(surface, BLUE, [self.xPosisjon, self.yPosisjon, 25, 25])

    def endreRetning(self):
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy

        if self.xPosisjon <= 100 or self.xPosisjon > WIDTH - 125:
            self.vx *= -1

        if self.yPosisjon > HEIGHT - 25 or self.yPosisjon < 0:
            self.vy *= -1

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)


class Menneske(Spillobjekt):
    def __init__(self, fart, poeng, holderSau):
        super().__init__(rd.randint(0, 100 - 25), rd.randint(0, HEIGHT - 25))
        self.fart = fart
        self.poeng = poeng
        self.holderSau = holderSau

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

    #Liten "sikkerhets rektangel foran det faktiske rektangelet. Forhindrer at kollisjon alltid er True, slik at man aldri kommer seg vekk fra hindringen."
    def hentNesteRektangel(self, dx, dy):
        return pg.Rect(self.xPosisjon + dx, self.yPosisjon + dy, 25, 25)

    def beveg(self, hindringer):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if not any(self.hentNesteRektangel(-5,0).colliderect(hindring.hentRektangel()) for hindring in hindringer):
                self.xPosisjon += -5
        if keys[pg.K_RIGHT]:
            if not any(self.hentNesteRektangel(5,0).colliderect(hindring.hentRektangel()) for hindring in hindringer):
                self.xPosisjon += 5
        if keys[pg.K_DOWN]:
            if not any(self.hentNesteRektangel(0,2).colliderect(hindring.hentRektangel()) for hindring in hindringer):
                self.yPosisjon += 5
        if keys[pg.K_UP]:
            if not any(self.hentNesteRektangel(0,-2).colliderect(hindring.hentRektangel()) for hindring in hindringer):
                self.yPosisjon += -5
        


class Hindring(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(100, WIDTH - 125), rd.randint(0, HEIGHT - 25))

    def tegnHindring(self):
        pg.draw.rect(surface, BLACK, [self.xPosisjon, self.yPosisjon, 25, 75])
    
    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 75)


class Sau(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(WIDTH - 100, WIDTH-25), rd.randint(0,HEIGHT - 25))

    def tegnSau(self):
        pg.draw.rect(surface, GREEN, [self.xPosisjon, self.yPosisjon, 25, 25])



    



# Oppretter menneskeobjektet
menneske = Menneske(0, 0, False)

W = 25
H = 25

spillbrett = Spillbrett()

# Lager 3 sauer som skal være der fra start
for i in range(0,3):
    hindring = Hindring()
    spillbrett.leggTilSpillObjekt(hindring)
    sau = Sau()
    spillbrett.leggTilSpillObjekt(sau)

spokelse = Spokelse()
spillbrett.leggTilSpillObjekt(spokelse)


print("Spillet starter med 3 spokelser")

# Spill-lokken
while run:
    # Sorger for at lokken kjores i korrekt hastighet
    clock.tick(FPS)

    # Gar gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi onsker a lukke vinduet
        if event.type == pg.QUIT:
            run = False  # Spillet skal avsluttes

    # Kaller menneske bevegmetoden
    menneske.beveg(spillbrett.hindringer)

    if any(menneske.hentRektangel().colliderect(hindring.hentRektangel()) for hindring in spillbrett.hindringer):
        print("Kollisjon mellom menneske og hindring")

    if any(menneske.hentRektangel().colliderect(spokelse.hentRektangel()) for hindring in spillbrett.spokelser):
        print("Kollisjon mellom menneske og spokelse")



    # Fyller skjermen med en farge
    surface.fill(WHITE)
    pg.draw.rect(surface, LIGHTYELLOW, [0, 0, 100, HEIGHT])
    pg.draw.rect(surface, LIGHTYELLOW, [WIDTH - 100, 0, 100, HEIGHT])
    pg.draw.rect(surface, BABYBLUE, [100, 0, WIDTH - 200, HEIGHT])

    # Tegner Menneske
    pg.draw.rect(surface, RED, [menneske.xPosisjon, menneske.yPosisjon, W, H])

    # Tegner spokelsene
    for spokelse in spillbrett.spokelser:
        spokelse.tegnSpokelse()
        spokelse.endreRetning()

    for hindring in spillbrett.hindringer:
        hindring.tegnHindring()

    for sau in spillbrett.sauer:
        sau.tegnSau()
      


    # "Flipper" displayet for a vise hva vi har tegnet
    pg.display.flip()

# Avslutter pygame
pg.quit()
sys.exit()

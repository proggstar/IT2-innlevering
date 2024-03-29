#Importerer biblioteker
import pygame as pg
import sys
import random as rd
import time

# Initierer pygame
pg.init()

#Tekst for poengscore
font = pg.font.SysFont('Arial', 20)
tekst = "Poeng:"
poeng= 0

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


#Bakgrunn
background_img1 = pg.image.load('stein.png')
background_img1 = pg.transform.scale(background_img1, (300, 300))
background_img2 = pg.image.load('stein.png')
background_img2 = pg.transform.scale(background_img2, (300, 300))
background_img3 = pg.image.load('stein.png')
background_img3 = pg.transform.scale(background_img3, (300, 300))
background_img4 = pg.image.load('stein.png')
background_img4 = pg.transform.scale(background_img4, (300, 300))
green_img = pg.image.load('green.png')
green_img = pg.transform.scale(green_img, (100, 600))

#Bilder til objekter
ghost_img = pg.image.load('ghost.png')
ghost_img = pg.transform.scale(ghost_img, (30, 30))
sau_img = pg.image.load('sau.png')
sau_img = pg.transform.scale(sau_img, (25, 25))
gjerde_img = pg.image.load('gjerde.png')
gjerde_img = pg.transform.scale(gjerde_img, (25, 75))
menneske_img = pg.image.load('menneske.png')
menneske_img = pg.transform.scale(menneske_img, (25, 25))

#Lydeffekt
poeng_sfx = pg.mixer.Sound('poeng.mp3')
gameover_sfx = pg.mixer.Sound('gameover.mp3')

# Lager en overflate vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjøres
run = True

# Klasser
class Spillbrett:
    spokelser = [] # Liste av Spøkelse
    hindringer = [] # Liste av Hindring
    sauer = [] # Liste av Sau 

    def leggTilSpillObjekt(self, spillobjekt):
        #Bruker "ifinstance" for å skille ut objektene og legge til å riktig liste
        if isinstance(spillobjekt, Spokelse):
            self.spokelser.append(spillobjekt)
         
        #while løkke for å lage en ny hindring som ikke blir lagt til oppå en eksisterende hindring
        #Løkken kjøres helt til det er funnet et objekt-hindring, som kan legge til i listen hindringer
        elif isinstance(spillobjekt, Hindring):
            run = True
            while run:
                ny_hindring = Hindring()
                if not any(hindring.hentRektangel().colliderect(ny_hindring.hentRektangel()) for hindring in self.hindringer):
                    self.hindringer.append(ny_hindring)
                    run = False
        #while løkke for å lage en ny sau som ikke blir lagt til oppe en eksisterende sau
        #Løkken kjøres helt til det er funnet et objekt-sau, som kan legge til i listen sauer 
        elif isinstance(spillobjekt, Sau):
            run = True
            while run:
                ny_sau = Sau()
                if not any(sau.hentRektangel().colliderect(ny_sau.hentRektangel()) for sau in self.sauer):
                    self.sauer.append(ny_sau)
                    run = False
                

    def fjernSpillObjekt(self, spillobjekt):
        #Bruker "ifinstance" for å skille ut og fjerne riktig objekt
        if isinstance(spillobjekt, Spokelse):
            self.spokelser.remove(spillobjekt)
            
        elif isinstance(spillobjekt, Hindring):
            self.hindringer.remove(spillobjekt)
            
        else:
            self.sauer.remove(spillobjekt)
            
    #Funksjon for poeng
    def antallPoeng(self):
        text_img = font.render(f"{tekst} {poeng}", True, BLACK)
        surface.blit(text_img, (10, 25))


class Spillobjekt:
    def __init__(self, xPosisjon, yPosisjon):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon

    def settPosisjon(self, x, y):
        self.xPosisjon = x
        self.yPosisjon = y

    def hentPosisjon(self):
        return (self.xPosisjon, self.yPosisjon)

class Spokelse(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(100, WIDTH - 200), rd.randint(0, HEIGHT - 25))
        self.vx = 3
        self.vy = 3

    def tegnSpokelse(self):
        #pg.draw.rect(surface, BLUE, [self.xPosisjon, self.yPosisjon, 25, 25])
        surface.blit(ghost_img,(self.xPosisjon, self.yPosisjon))
        self.yPosisjon += self.vy
    
    def endreRetning(self):
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy
        
        if self.xPosisjon <= 100 or self.xPosisjon > WIDTH - 125:
            self.vx *= -1

        if self.yPosisjon > HEIGHT - 25 or self.yPosisjon < 0:
            self.vy *= -1

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

    def frys(self):
        self.vx = 0
        self.vy = 0

class Menneske(Spillobjekt):
    def __init__(self, fart, poeng, holderSau):
        super().__init__(rd.randint(0, 100 - 25), rd.randint(0, HEIGHT - 25))
        self.fart = fart
        self.poeng = poeng
        #Nødvendige variabler for bæring av sau 
        self.holderSau = False
        self.sauSomErHoldt = None 

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

    #Liten "sikkerhets rektangel" foran det faktiske rektangelet.
    #Forhindrer at kollisjon alltid = True, slik at man aldri kommer seg vekk/stuck fra hindringen.
    def hentNesteRektangel(self, dx, dy):
        return pg.Rect(self.xPosisjon + dx, self.yPosisjon + dy, 25, 25)

    def settHastighet(self, vx,vy):
        self.vx = vx
        self.vy = vy

    def beveg(self, hindringer):
        keys = pg.key.get_pressed()
        #Bevegelse for menneske: kollisjon med hindringer og kant av spillbrett 
        if keys[pg.K_LEFT]:
            if not any(self.hentNesteRektangel(-5,0).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.xPosisjon >= 0:
                self.xPosisjon -= self.vx
        if keys[pg.K_RIGHT]:
            if not any(self.hentNesteRektangel(5,0).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.xPosisjon <= WIDTH - W:
                self.xPosisjon += self.vx
        if keys[pg.K_DOWN]:
            if not any(self.hentNesteRektangel(0,5).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.yPosisjon <= HEIGHT - H:
                self.yPosisjon += self.vy
        if keys[pg.K_UP]:
            if not any(self.hentNesteRektangel(0,-5).colliderect(hindring.hentRektangel()) for hindring in hindringer) and self.yPosisjon >= 0:
                self.yPosisjon -= self.vy

class Hindring(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(100, WIDTH - 125), rd.randint(0, HEIGHT - 25))

    def tegnHindring(self):
        #pg.draw.rect(surface, BLACK, [self.xPosisjon, self.yPosisjon, 25, 75])
        surface.blit(gjerde_img,(self.xPosisjon, self.yPosisjon))
    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 75)


class Sau(Spillobjekt):
    def __init__(self):
        super().__init__(rd.randint(WIDTH - 100, WIDTH-25), rd.randint(0,HEIGHT - 25))

    def tegnSau(self):
        #pg.draw.rect(surface, GREEN, [self.xPosisjon, self.yPosisjon, 25, 25])
        surface.blit(sau_img,(self.xPosisjon, self.yPosisjon))

    def hentRektangel(self):
        return pg.Rect(self.xPosisjon, self.yPosisjon, 25, 25)

# Oppretter menneskeobjektet
menneske = Menneske(0, 0, False)
menneske.settHastighet(5,5)

spillbrett = Spillbrett()

W = 25
H = 25

# Lager 3 sauer og hindringer som skal være der fra start
for i in range(0,3):
    hindring = Hindring()
    spillbrett.leggTilSpillObjekt(hindring)
    sau = Sau()
    spillbrett.leggTilSpillObjekt(sau)
    
#Lager 1 spøkelse som skal være der fra start
spokelse = Spokelse()
spillbrett.leggTilSpillObjekt(spokelse)

# Spill-lokken
while run:
    # Sørger for at løkken kjøres i korrekt hastighet
    clock.tick(FPS)

    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False  # Spillet skal avsluttes

    # Kaller menneske bevegmetoden
    menneske.beveg(spillbrett.hindringer)

    #Sjekker for kollisjon mellom spøkelser og menneske
    if any(menneske.hentRektangel().colliderect(spokelse.hentRektangel()) for spokelse in spillbrett.spokelser):
        for spokelse in spillbrett.spokelser:
            gameover_sfx.play()
            spokelse.frys()
            font = pg.font.SysFont('Arial', 160)
            tekst = "game over"
            poeng = ""
            time.sleep(1)
            run = False
            break
            
        menneske.settHastighet(0,0)
    
    
    for sau in spillbrett.sauer:
        #Forhindrer å plukke opp fler sauer
        if not menneske.holderSau:
            #Bærer sau
            if menneske.hentRektangel().colliderect(sau.hentRektangel()):
                menneske.holderSau = True
                menneske.sauSomErHoldt = sau
                menneske.settHastighet(3, 3)

    #Når sau er på venstre frisone
    if menneske.holderSau and 30 < menneske.sauSomErHoldt.hentPosisjon()[0] < 100:
        #Setter sau langt vekk
        menneske.sauSomErHoldt.settPosisjon(-100,-100)
        #Nye objekter
        spillbrett.leggTilSpillObjekt(Sau())
        spillbrett.leggTilSpillObjekt(Spokelse())
        spillbrett.leggTilSpillObjekt(Hindring())
        poeng += 1
        poeng_sfx.play() 
        menneske.settHastighet(5, 5)
        menneske.sauSomErHoldt = None
        menneske.holderSau = False
        
    # Sjekker om en menneske som bærer sau objektet kolliderer med en annen sau
    if menneske.holderSau == True:
        for sau1 in spillbrett.sauer:
            for sau2 in spillbrett.sauer:
                if sau1 != sau2 and menneske.holderSau and menneske.sauSomErHoldt is sau1 and sau1.hentRektangel().colliderect(sau2.hentRektangel()):
                
                    spokelse.frys()
                    font = pg.font.SysFont('Arial', 160)
                    tekst = "game over"
                    poeng = ""
                    time.sleep(1)
                    gameover_sfx.play()
                    run = False
                    break
                   
                    
    #Plasserer sau "oppå" menneske
    for sau in spillbrett.sauer:
        if menneske.holderSau and sau is menneske.sauSomErHoldt:
            sau.settPosisjon(menneske.hentPosisjon()[0]+5, menneske.hentPosisjon()[1]+20)
        sau.tegnSau()

    #pg.draw.rect(surface, LIGHTYELLOW, [0, 0, 100, HEIGHT])
    surface.blit(green_img,(0, 0))
    
    #pg.draw.rect(surface, LIGHTYELLOW, [WIDTH - 100, 0, 100, HEIGHT])
    surface.blit(green_img,(WIDTH-100, 0))
    
    #pg.draw.rect(surface, BABYBLUE, [100, 0, WIDTH - 200, HEIGHT])
    
    #Tegner bakgrunnen
    surface.blit(background_img1, (100, 0))
    surface.blit(background_img1, (400, 0))
    surface.blit(background_img1, (100, 300))
    surface.blit(background_img1, (400, 300))

    # Tegner Menneske
    #pg.draw.rect(surface, RED, [menneske.xPosisjon, menneske.yPosisjon, W, H])
    surface.blit(menneske_img,(menneske.xPosisjon, menneske.yPosisjon))
    
    # Tegner spokelsene
    for spokelse in spillbrett.spokelser:
        spokelse.tegnSpokelse()
        spokelse.endreRetning()

    # Tegner spokelsene
    for hindring in spillbrett.hindringer:
        hindring.tegnHindring()

    # Tegner spokelsene
    for sau in spillbrett.sauer:
        sau.tegnSau()
      
    #Poeng score
    spillbrett.antallPoeng()
        
    # "Flipper" displayet for a vise hva vi har tegnet
    pg.display.flip()

# Avslutter pygame
pg.quit()
sys.exit()




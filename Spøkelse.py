


class Spøkelse(Spillobjekt):
    vx = 3
    vy = 3

    def tegnSpøkelse(self):
        pg.draw.rect(surface, BLUE, [self.xPosisjon, self.yPosisjon, 25, 25])

    def endreRetning(self):

        self.xPosisjon += vx
        self.yPosisjon += vy

    if self.xPosisjon <= 100:
        vx *= -1
        x = WIDTH - w
    
    if x < 0:
        vx *= -1
        x = 0
       
    if (y+h) > HEIGHT:
        yx *= -1
          
    if y < 0:
        yx *= -1
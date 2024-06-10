# pygame-exercise-snowscape.py

import random
import pygame as pg
from pygame import mixer

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
GRAY = (140, 140, 140)
WIDTH = 1460
HEIGHT = 900
TITLE = "RICHMOND SIMULATOR"

#Assets and Rescaling
ketchupsize = (100,100)
kcup1 = pg.transform.scale(pg.image.load("./Images/ketchup.png"), ketchupsize)
kcup2 = pg.transform.scale(pg.image.load("./Images/ketchup2.png"), ketchupsize)
kcup3 = pg.transform.scale(pg.image.load("./Images/ketchup3.png"), ketchupsize)
kcups = [kcup1, kcup2, kcup3]
ketchuppic = random.choice(kcups)

class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #could have super inited but huh

        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
BackGround = Background("./Images/streetview.png", [0,0])

class Fumo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        DEFAULT_IMAGE_SIZE = (70, 60)

        self.image = pg.transform.scale(pg.image.load("./Images/man.png"), DEFAULT_IMAGE_SIZE)
 
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 650
        print(f"self.rect.centerx,self.rect.centery")
        self.splatter = False
    def update(self):
        # Limiter for x and -x and replace picture if cleaved by car
        if self.rect.x < 600:
            self.rect.x = 600
        if self.rect.x > 790:
            self.rect.x = 790
        if self.splatter == True:
            self.image = ketchuppic
            
# Assets and Positions
CSIZE = (130,130)
crash1 = pg.transform.scale(pg.image.load("./Images/crash1.png"), CSIZE)
crash2 = pg.transform.scale(pg.image.load("./Images/crash2.png"), CSIZE)
crash3 = pg.transform.scale(pg.image.load("./Images/crash3.png"), CSIZE)
crashpic = [crash1,crash2,crash3]
carcoord = [640,705,765,825]
# randomized car pics for variety
ISIZE = (50,100)
car1 = pg.transform.scale(pg.image.load("./Images/car1.png"), ISIZE)
car2 = pg.transform.scale(pg.image.load("./Images/car2.png"), ISIZE)
carpic = [car1,car2]

class Snow(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = random.choice(carpic)

        self.rect = self.image.get_rect()

        self.vel_y = random.randint(3,45)
        # Initial coords
        self.rect.centerx = random.choice(carcoord)
        self.rect.centery = 1
        self.accel_y = 0.1

        self.crashed = False
    def update(self):
        self.vel_y -= self.accel_y
        # self.accel_y += 0.002
        if not self.crashed:
            self.rect.y += self.vel_y


    def crash(self):
        if not self.crashed:
            self.image = random.choice(crashpic)
            self.crashed = True

            
def main():
    pg.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pg.display.set_mode(size)
    pg.display.set_caption(TITLE)
    font=pg.freetype.SysFont(None, 34)
    font.origin=True

    # ----- LOCAL VARIABLES
    done = False
    clock = pg.time.Clock()

    # Create a snow sprites group
    allsprites = pg.sprite.Group()
    snow_sprites = pg.sprite.Group()

    fumo = Fumo()
    snow = Snow()
    allsprites.add(snow)
    snow_sprites.add(snow)
    allsprites.add(fumo)


    # ----- MAIN LOOP
    # music loop 
    file = './Images/pgbm.mp3'
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    while not done:
        
        pg.display.flip()
        clock.tick(60)

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        # Timer Function (stops counting when fumo.splatter = true)
        if fumo.splatter == False:
            ticks=pg.time.get_ticks()
            millis=ticks%1000
            seconds=int(ticks/1000 % 60)
            minutes=int(ticks/60000 % 24)
            out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        font.render_to(screen, (300, 230), out, pg.Color('black'))

        # print(fumo.rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    fumo.rect.x -= 65
                if event.key == pg.K_RIGHT:
                    fumo.rect.x += 65
        

        # ----- LOGIC
        allsprites.update()
        

        
        # Clone car for every car that falls to the top or the bottom
        for snow in snow_sprites:
            
            if snow.rect.bottom >= 850 or snow.rect.bottom <=-10:
                if not snow.crashed:
                    snow.crash()
                    snow = Snow()
                    allsprites.add(snow)
                    snow_sprites.add(snow)

        # Check to see if fumo has collided with any snow
        snow_collided = pg.sprite.spritecollide(fumo, snow_sprites, False)

        if snow_collided:
            fumo.splatter = True
        
        # ----- RENDER
  

        # Draw all the sprite groups
        allsprites.draw(screen)


        # ----- UPDATE DISPLAY
        pg.display.flip()
        clock.tick(60)

    pg.quit()


def random_coords():
    x, y = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    return x, y


if __name__ == "__main__":
    main()
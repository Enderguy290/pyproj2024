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

class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
BackGround = Background("./Images/streetview.png", [0,0])

class Fumo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        DEFAULT_IMAGE_SIZE = (100, 100)

        self.image = pg.transform.scale(pg.image.load("./Images/file.png"), DEFAULT_IMAGE_SIZE)
 
        
        
        self.rect = self.image.get_rect()
        self.rect.x = 520
        self.rect.y = 390
    def update(self):
        self.rect.centerx = pg.mouse.get_pos()[0]
        self.rect.centery = pg.mouse.get_pos()[1]
CSIZE = (100,100)
crash1 = pg.transform.scale(pg.image.load("./Images/crash1.png"), CSIZE)
crash2 = pg.transform.scale(pg.image.load("./Images/crash2.png"), CSIZE)
crash3 = pg.transform.scale(pg.image.load("./Images/crash3.png"), CSIZE)
crashpic = [crash1,crash2,crash3]
class Snow(pg.sprite.Sprite):
    def __init__(self, width: int):
        
        """
        Params:
            width: width of snow in px
        """
        super().__init__()
        ISIZE = (75,75)
        self.image = pg.transform.scale(pg.image.load("./Images/icicle.png"), ISIZE)

        self.rect = self.image.get_rect()

        self.vel_y = random.randint(5,8)
        # Initial coords
        self.rect.centerx = random.randint(1,1280)
        self.rect.centery = 1

        self.crashed = False
    def update(self):
        if self.rect.y < 800:
            self.rect.y += self.vel_y
        elif not self.crashed:
            self.image = random.choice(crashpic)
            self.crashed = True
            


def main():
    pg.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pg.display.set_mode(size)
    pg.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pg.time.Clock()

    # Create a snow sprites group
    allsprites = pg.sprite.Group()
    snow_sprites = pg.sprite.Group()

    fumo = Fumo()
    # Create more snow
    for _ in range(15):
        snow = Snow(10)
        allsprites.add(snow)
        snow_sprites.add(snow)

    allsprites.add(fumo)


    # ----- MAIN LOOP
    file = './Images/735623.mp3'
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    while not done:
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        # -- Event Handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        # ----- LOGIC
        allsprites.update()

        # Check to see if fumo has collided with any snow
        snow_collided = pg.sprite.spritecollide(fumo, snow_sprites, False)

        if snow_collided:
            done = True

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
# This file was created by: Patrick Von Ploennies
# Content inspired by: Chris Bradfield
# Solemnly swear to create concise and informative comments.
 
'''
# The game engine consists of 4 basic components
# Input - keys, buttons, voice, mouse, touch, breath, movement, control stick
# Process - input processed (direction of control, magnitude)
# Output - Draw new frames pixels, sounds, haptics (senses)
# (Store)

GOALS: Defeat every boss in sequence
RULES: Time, Movement, Health
FEEDBACK: Enemey hit sounds & effects, Health loss sounds.
FREEDOM: movement and shooting thats it
'''
 
import pygame as pg
from os import path

from settings import *
from sprites import *
from utils import *


# The Game class is a blueprint for the entire game.
class Game:
    def __init__(self):

        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

        self.clock = pg.time.Clock()

        self.running = True
        self.playing = True

        self.dt = self.clock.tick(FPS) / 1000

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir,'sounds')
        self.map = Map(path.join(self.game_dir,map))
 
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()

        for i in range(15):
            proj = EnemyProjectile(self,WIDTH/2,0 ,45+i*15,150)
        
        
        for row , tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row,1,1)
                    
                if tile == "P":
                    self.player = Player( self, col,row)

                if tile == "E":
                    self.enemy = Enemy( self, col, row )

    #  draw text on the screen somewhere
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        # instance of font clas.
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def run(self):

        # main loop
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000

            self.events() # input
            self.update() # process
            self.draw() # output

    # This code handles processing player input.
    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

                self.running = False


    # Update all sprites.
    def update(self):
        self.all_sprites.update()

    # Draw the current screen
    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text("FPS: " + str(floor(1/self.dt)), 24, WHITE, WIDTH/ 2, HEIGHT / 4)
        pg.display.flip()

if __name__ == "__main__": #mc
    g = Game()

g.new()

while g.running:

    g.run()

pg.quit()
 
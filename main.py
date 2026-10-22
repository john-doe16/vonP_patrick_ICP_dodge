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
import numpy as np

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

        self.highscore = 0
        self.coins = 0

        self.dt = self.clock.tick(FPS) / 1000

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "SaveFile.txt")
        self.img_dir = path.join(self.game_dir, 'images')
        self.map = Map(path.join(self.game_dir,map))

        # sound handling #
        self.snd_dir = path.join(self.game_dir,'sounds')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir,'coin.wav'))
        self.background_music = path.join(self.snd_dir,'bg_music.wav')


        # attempt to find file, if not build a file
        try:
            with open(self.game_save_file, "x", encoding="utf-8") as file:
                file.write("Hello, World!")
            print("File created successfully.")
        except FileExistsError:
            print("File already exists. No action taken.")

        # open file and try to set high score with except set high score to zero
        with open(self.game_save_file, 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
                print("high score is zero")
 
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()

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

                if tile == "C":
                    self.coin = Coin(self, col,row,1,1)

        pg.mixer.music.load(self.background_music)
        pg.mixer.music.play(loops=-1)

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
                with open(path.join(self.game_dir, self.game_save_file), 'w') as f:
                    if self.highscore > self.coins:
                        f.write(str(self.highscore))
                    else:
                        f.write(str(self.coins))
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
        self.draw_text(f"Coins: {self.coins}", 24, WHITE, WIDTH/ 2, HEIGHT / 9)
        self.draw_text(f"Highscore: {self.highscore}", 24, WHITE, WIDTH/ 2, HEIGHT / 13)
        pg.display.flip()

if __name__ == "__main__": #mc
    g = Game()

g.new()

while g.running:

    g.run()

pg.quit()
 
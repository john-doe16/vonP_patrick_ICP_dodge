from settings import *
from utils import *
import pygame as pg
import math
from math import floor
from pygame.sprite import Sprite
from os import path
from random import randint

vec = pg.math.Vector2

# Create player Class with Sprite super

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite,group,dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)

        if hits:

            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2

            sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)

        if len(hits) > 0:

            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2

            sprite.vel.y = 0
        sprite.hit_rect.centery = sprite.pos.y

class Wall(Sprite):

    def __init__ (self, game, x,y, sx,sy):

        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface( (TILESIZE * sx,TILESIZE * sy) )
        self.image.fill( GREEN )
        self.rect = self.image.get_rect()

        self.x, self.y = x,y

        self.x = x * TILESIZE
        self.y = y *  TILESIZE

    def update (self):
        self.rect.x = self.x
        self.rect.y = self.y

class TileSurface(Sprite):

    def __init__ (self, game, x,y):

        self.game = game
        self.groups = game.all_sprites, game.all_tiles
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface( (TILESIZE,TILESIZE) )
        self.image.fill( BLUE )
        self.rect = self.image.get_rect()
        self.varient = None

        self.x, self.y = x,y

        self.x = x * TILESIZE
        self.y = y *  TILESIZE

    def update (self):
        self.rect.x = self.x
        self.rect.y = self.y

    def set_varient (self,varient):
        self.varient = varient
        if varient == "ice":
            self.image.fill(CYAN)
    

class Particle(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((TILESIZE // 4, TILESIZE // 4))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.pos = vec(x, y)
        self.vel = vec(randint(-180, 180), randint(-180, 180))
        self.rect.center = self.pos

        self.countdown = Cooldown()
        self.countdown.event_time = math.floor(pg.time.get_ticks() / 1000)

    def update(self):
        self.countdown.ticking()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if self.countdown.delta > 1:
            self.kill()

class Coin(Sprite):

    def __init__ (self, game, x,y, sx,sy):

        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface( (TILESIZE * sx,TILESIZE * sy) )
        pg.draw.circle(self.image,YELLOW, (TILESIZE/2,TILESIZE/2), TILESIZE/2)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()


        self.x, self.y = x,y

        self.x = x * TILESIZE
        self.y = y *  TILESIZE

    def update (self):
        self.rect.x = self.x
        self.rect.y = self.y

class Player(Sprite):

    def __init__ (self, game, x,y):

        print("player created")

        self.game = game
        #provides us with raster images for use in animation
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)

        # Sprite and size defs
        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"sprite_sheet.png"))
        self.image = pg.Surface( (TILESIZE,TILESIZE) )
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.cofric = -0.1
        self.current_tile = None

        self.hit_rect = PLAYER_HIT_RECT

        # initialize animation related variables
        # init frame at 0
        self.current_frame = 0
        self.last_update = 0
        # states?
        self.jumping = False
        self.moving = False

        self.load_images()

    # get player input
    def get_keys(self):

        self.acc = vec(0,0)

        keys = pg.key.get_pressed()

        if keys[KEYBINDS["MoveLeft"]]:
            self.acc.x = -PLAYER_ACC
        if keys[KEYBINDS["MoveRight"]]:
            self.acc.x = PLAYER_ACC

        if keys[KEYBINDS["MoveUp"]]:
            self.acc.y = -PLAYER_ACC
        if keys[KEYBINDS["MoveDown"]]:
            self.acc.y = PLAYER_ACC

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]

    def animate(self):
        now = pg.time.get_ticks()
      
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                # when show nedxt frame
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]                
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            elif self.moving:
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                    bottom = self.rect.bottom
                    self.image = self.moving_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

    def update(self):
        self.get_keys()

        if self.current_tile == "I":
            self.cofric = -0.01
        else:
            self.cofric = -0.1

        self.acc.x += self.vel.x * self.cofric
        self.acc.y += self.vel.y * self.cofric

        self.vel += self.acc

        self.pos.x += (self.vel.x + 0.5 * self.acc.x) * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')

        self.pos.y += (self.vel.y + 0.5 * self.acc.y) * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        self.rect.center = self.hit_rect.center
        hits = pg.sprite.spritecollide(self,self.game.all_coins,False, collide_hit_rect)

        if hits:
            for i in range(25):
                print(i)
                Particle(self.game,self.pos.x,self.pos.y)
            hits[0].kill()
            self.game.coins += 1
            self.game.pickup_snd.play()

        col = floor(self.pos.x / TILESIZE)
        row = floor(self.pos.y / TILESIZE)
        self.current_tile = self.game.map.data[row][col]
        
class Enemy(Sprite):

    def __init__ (self, game, x,y):

        self.game = game

        #provides us with raster images for use in animation

        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)

        # Sprite and size defs

        self.scale = 1

        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"enemy_sprite_sheet.png"))
        self.image = pg.Surface( (TILESIZE * self.scale,TILESIZE * self.scale))
        self.image = self.spritesheet.get_image(0,0,TILESIZE * self.scale,TILESIZE * self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.speed = -100

        self.vel = vec(0,0)

        self.pos = vec(x,y) * TILESIZE

        self.hit_rect = ENEMY_HIT_RECT.copy()

        # initialize animation related variables
        # init frame at 0

        self.current_frame = 0
        self.last_update = 0
        # states?
        self.jumping = False
        self.moving = False

        self.load_images()

    def move_player(self):
        player = self.game.player
        if self.pos - player.pos == 0:
            return
        direction = (self.pos - player.pos).normalize()

        self.vel = direction * self.speed

    




    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]

    def animate(self):
        now = pg.time.get_ticks()
      
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                # when show nedxt frame
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]                
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            elif self.moving:
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                    bottom = self.rect.bottom
                    self.image = self.moving_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

    def update(self):
        self.move_player()

        self.pos += self.vel * self.game.dt

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')


        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        self.rect.center = self.hit_rect.center

class EnemyProjectile(Sprite):

    def __init__(self,game,x,y ,angle,speed):

        self.game = game
        self.groups = game.all_sprites, game.projectiles
        Sprite.__init__(self, self.groups)

        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE

        self.x = x
        self.y = y

        self.angle = math.radians(angle)
        self.speed = speed

        self.image = pg.Surface( (TILESIZE,TILESIZE) )
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        self.x += math.cos(self.angle) * self.speed * self.game.dt
        self.y += math.sin(self.angle) * self.speed * self.game.dt

        self.rect.x = self.x
        self.rect.y = self.y

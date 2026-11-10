from settings import *
from utils import *
import pygame as pg
import math
from math import floor
from pygame.sprite import Sprite
from os import path
from random import randint
from BossConfig import *

vec = pg.math.Vector2

def get_sprite_scale(sprite):
    return SPRITE_SCALE * sprite.SCALE


def scale_sprite_image(image, scale):
    if scale == 1:
        return image
    size = (max(1, round(image.get_width() * scale)),
            max(1, round(image.get_height() * scale)))
    return pg.transform.scale(image, size)


# Hit Rect
def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

# Check if the player is touching a wall
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

# Wall Classes
class Wall(Sprite):
    SCALE = 1.0

    def __init__ (self, game, x,y, sx,sy):

        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
        self.image = pg.Surface((max(1, round(TILESIZE * sx * self.scale)),
                     max(1, round(TILESIZE * sy * self.scale))))
        self.image.fill( GREEN )
        self.rect = self.image.get_rect()

        self.x, self.y = x,y

        self.x = x * TILESIZE
        self.y = y *  TILESIZE

    # Slightly useless.
    def update (self):
        self.rect.x = self.x
        self.rect.y = self.y

# Define a ground surface.
class TileSurface(Sprite):
    SCALE = 1.0

    def __init__ (self, game, x,y):

        self.game = game
        self.groups = game.all_sprites, game.all_tiles
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
        size = max(1, round(TILESIZE * self.scale))
        self.image = pg.Surface((size, size))
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
    

# Temp Particle class, Should be cleaned up ltr.

# MAKE TIHS LATER ITS REDUNDENT


class Particle(Sprite):
    SCALE = 0.8
    LIFETIME = 0.5

    def tween(self, start, end, age, lifetime):
        t = min(age / lifetime, 1)
        return start + (end - start) * t

    def __init__(self, game, x, y,part_type = None,params = None):
        self.part_type = part_type
        self.params = params
        self.game = game
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)

        self.size_goal = False
        self.alpha_goal = 0

        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"Wave1.png"))

        if self.part_type == None:
            self.vel = vec(randint(-180, 180), randint(-180, 180))
            self.alpha_goal = 0
            return
        if self.part_type == "Expand":
            self.LIFETIME = 0.5
            self.size_goal = 1.3
            self.alpha_goal = 0
        if self.part_type == "Coin":
            self.spritesheet = Spritesheet(path.join(self.game.img_dir,"coin.png"))
            self.LIFETIME = 0.25
            self.size_goal = 1.1
            self.alpha_goal = 0

        self.scale = get_sprite_scale(self)
        self.original_image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE).convert_alpha()
        self.original_image.set_colorkey((0,0,0))
        self.image = scale_sprite_image(self.original_image, self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.age = 0
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.rect.center = self.pos

        self.countdown = Cooldown()
        self.countdown.event_time = math.floor(pg.time.get_ticks() / 1000)


    def update(self):
        # Move based on countdown class.
        self.countdown.ticking()
        self.pos += (self.vel * self.game.dt)
        self.age += self.game.dt

        if self.size_goal is not False:
            scale = self.tween(self.scale, self.size_goal, self.age, self.LIFETIME)
            self.image = scale_sprite_image(self.original_image, scale)
            self.image.set_colorkey((0,0,0))
        if self.alpha_goal is not False:
            self.image.set_alpha(self.tween(255,0, self.age, self.LIFETIME))
        self.rect = self.image.get_rect(center=self.pos)

        if self.age >= self.LIFETIME:
            self.kill()

# Define a pick-up able coin, should be replaced ltr.
class Coin(Sprite):
    SCALE = 1

    def __init__ (self, game, x,y, sx,sy):

        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
    # Draw the image
        self.image = pg.image.load(path.join(self.game.img_dir, "coin.png"))
        self.image = pg.transform.scale(
            self.image,
            (max(1, round(TILESIZE * sx * self.scale)),
             max(1, round(TILESIZE * sy * self.scale))),
        )
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))


        self.x, self.y = x,y

        self.x = x
        self.y = y

    def update (self):
        self.y += 50 * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y

# Define the user-controlled player sprite
class Player(Sprite):
    SCALE = 2.0

    def __init__ (self, game, x,y):

        print("player created")

        self.game = game
        #provides us with raster images for use in animation
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
        # Sprite and size defs
        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"sprite_sheet.png"))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image = scale_sprite_image(self.image, self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.total_shots = 0
        self.lives = 5
        self.invincibility = False

        for i in range(self.lives):
            Heart(self.game, 15 + (i * TILESIZE), 15)

        # cooldowns:
        self.countdown = Cooldown(50)
        self.invincibility_cooldown = Cooldown(1000)
        self.last_shot = 0

        # Define movement parameters.
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.cofric = -0.1
        self.current_tile = None

        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.width = max(1, round(self.hit_rect.width * self.scale))
        self.hit_rect.height = max(1, round(self.hit_rect.height * self.scale))

        # initialize animation related variables
        # init frame at 0
        self.current_frame = 0
        self.last_update = 0
        self.last_pause = False
        # states?
        self.jumping = False
        self.moving = False

        self.load_images()

    # Fire projectiles
    def shoot(self):
        self.total_shots += 1
        if self.total_shots % 2 == 0:
            x_offset = - 5
        else:
            x_offset = 5
        self.game.shoot_snd.play()
        PlayerProjectile(self.game,self.pos.x + x_offset,self.pos.y - 25,-90,800)

    # get player input
    def get_keys(self):

        self.acc = vec(0,0)

        keys = pg.key.get_pressed()

        # Custom Keybinds 
        if keys[KEYBINDS["MoveLeft"]]:
            self.acc.x = -PLAYER_ACC
        if keys[KEYBINDS["MoveRight"]]:
            self.acc.x = PLAYER_ACC

        if keys[KEYBINDS["MoveUp"]]:
            self.acc.y = -PLAYER_ACC
        if keys[KEYBINDS["MoveDown"]]:
            self.acc.y = PLAYER_ACC

        if keys[KEYBINDS["Shoot"]]:
            delta = self.countdown.current_time - self.last_shot
            if delta > 1:
                self.shoot()
                self.last_shot = self.countdown.current_time

    def load_images(self):
        self.idle_frames = [
            scale_sprite_image(self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE), self.scale),
            scale_sprite_image(self.spritesheet.get_image(32, 0, TILESIZE, TILESIZE), self.scale),
        ]

    # Probably won't be used for now; remove later?
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

    def damage(self):
        if self.invincibility:
            return
        self.lives -= 1
        if len(self.game.all_ui.sprites()) > 0:
            self.game.blank()
            self.game.hit_snd.play()
            self.game.all_ui.sprites()[-1].kill()
            self.invincibility = True
            self.last_pause = self.invincibility_cooldown.current_time
            


    # Bloated update def.
    def update(self):
        self.get_keys()
        self.countdown.ticking()
        self.invincibility_cooldown.ticking()
        

        # Modify friction based off the current tile.
        if self.current_tile == "I":
            self.cofric = -0.01
        else:
            self.cofric = -0.1

        self.acc.x += self.vel.x * self.cofric
        self.acc.y += self.vel.y * self.cofric

        self.vel += self.acc

        # Check walls on each axis.
        self.pos.x += (self.vel.x + 0.5 * self.acc.x) * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')

        self.pos.y += (self.vel.y + 0.5 * self.acc.y) * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        screen_rect = self.game.screen.get_rect()
        before = self.hit_rect.center

        # Clamp the player position to prevent them from leaving the screen
        self.hit_rect.clamp_ip(screen_rect)

        if self.hit_rect.centerx != before[0]:
            self.pos.x = self.hit_rect.centerx
            self.vel.x = 0
        if self.hit_rect.centery != before[1]:
            self.pos.y = self.hit_rect.centery
            self.vel.y = 0

        self.rect.center = self.hit_rect.center

        self.rect.center = self.hit_rect.center
        hits = pg.sprite.spritecollide(self,self.game.all_coins,False, collide_hit_rect)

        delta = self.invincibility_cooldown.current_time - self.last_pause
        if delta > 1:
            self.invincibility = False
            self.last_pause = self.invincibility_cooldown.current_time
        

        # check hits.
        if hits:
            Particle(self.game,hits[0].rect.centerx,hits[0].rect.centery,"Coin")
            hits[0].kill()
            self.game.coins += 1
            self.game.pickup_snd.play()


        col = floor(self.pos.x / TILESIZE)
        row = floor(self.pos.y / TILESIZE)
        if row in self.game.map.data and col in self.game.map.data[row]:
            self.current_tile = self.game.map.data[row][col]
        else:
            self.current_tile = None


class Boss(Sprite):
    SCALE = 1.0

    def __init__ (self, game, x,y,boss_type):

        self.game = game
        self.x,self.y = x,y

        self.scale = get_sprite_scale(self)
        self.boss_type = boss_type

        self.groups = game.all_sprites

        # Define boss sprites.
        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"enemy_sprite_sheet.png"))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image = scale_sprite_image(self.image, self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.hit_rect = pg.Rect(x, y, self.rect.width, self.rect.height)

    def update(self):
        self.hit_rect.center = self.rect.center

        
class Enemy(Sprite):
    SCALE = 1.0

    def __init__ (self, game, x,y):

        self.game = game

        #provides us with raster images for use in animation

        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
        # Sprite and size defs

        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"enemy_sprite_sheet.png"))
        self.original_image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image = scale_sprite_image(self.image, self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.age = 0
        self.shoot_cooldown = Cooldown(50)
        self.last_shot = floor(pg.time.get_ticks() / 50)
        self.movement_cooldown = Cooldown(1)
        self.movement_cooldown.ticking()
        self.movement_cooldown.event_time = self.movement_cooldown.current_time

        self.health = 100
        self.hit_effect = False

        self.vel = vec(0,0)

        self.pos = vec(x,y) * TILESIZE

        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.width = max(1, round(self.hit_rect.width * self.scale))
        self.hit_rect.height = max(1, round(self.hit_rect.height * self.scale))

        # initialize animation related variables
        # init frame at 0

        self.current_frame = 0
        self.last_update = 0
        # states?
        self.jumping = False
        self.moving = False

        self.load_images()
        self.pos.y = self.y * TILESIZE
        self.pattern_off = randint(-500, 500)

    def damage(self):
        self.health -= 10

        self.hit_effect = True
        self.hit_time = self.current_frame

        self.image = self.original_image.copy()
        self.image.fill((255, 255, 255), special_flags=pg.BLEND_RGB_MAX)



        if self.health <= 0:
            Particle(self.game,self.rect.centerx,self.rect.centery,"Expand")
            self.game.death_snd.play()
            for i in range(5):
                Coin(self.game, self.rect.x + randint(-35, 35), self.rect.y + randint(-35, 35), 0.5, 0.5)
            self.kill()
    


    def move_pattern(self):
        self.movement_cooldown.ticking()
        pattern_time = self.movement_cooldown.delta / 1000 + self.pattern_off
        self.pos.x = self.game.width / 2 + (self.game.width / 2 - TILESIZE) * math.sin(pattern_time * 1.2)

    def load_images(self):
        self.idle_frames = [
            scale_sprite_image(self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE), self.scale),
            scale_sprite_image(self.spritesheet.get_image(32, 0, TILESIZE, TILESIZE), self.scale),
        ]

    # Redundent animate function.
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
        self.move_pattern()
        self.age += 1
        self.shoot_cooldown.ticking()
        if self.shoot_cooldown.current_time - self.last_shot >= 150 + randint(-50, 50):
            for i in range(20):
                proj = EnemyProjectile(self.game,self.pos.x,self.pos.y ,45+i*20,150)

            self.last_shot = self.shoot_cooldown.current_time

        if self.hit_effect:
            if pg.time.get_ticks() - self.hit_time >= 150:
                self.image = self.original_image.copy()
                self.hit_effect = False
                self.image.set_colorkey(BLACK)

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')


        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        self.rect.center = self.hit_rect.center


# Basic Player Projectile code
class PlayerProjectile(Sprite):
    SCALE = 0.8

    def __init__(self,game,x,y ,angle,speed):

        self.game = game
        self.groups = game.all_sprites, game.projectiles
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
        self.vel = vec(0,0)
        self.pos = vec(x,y)


        self.angle = math.radians(angle)
        self.speed = speed

        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"PlayerBullet.png"))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image = scale_sprite_image(self.image, self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

        self.rect.x,self.rect.y = self.pos.x,self.pos.y

    def update(self):
        self.pos.x += math.cos(self.angle) * self.speed * self.game.dt
        self.pos.y += math.sin(self.angle) * self.speed * self.game.dt

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        hits = pg.sprite.spritecollide(self,self.game.all_sprites,False,collide_hit_rect)

        if hits and hits[0]:
            hit_name = type(hits[0]).__name__
            if hit_name == "Enemy":
                hits[0].damage()
                self.kill()

class Heart(Sprite):
    SCALE = 1

    def __init__ (self, game, x,y):

        self.game = game
        self.groups = game.all_sprites, game.all_ui
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)

        # Draw the image

        self.image = pg.image.load(path.join(self.game.img_dir, "Heart.png"))
        self.image = pg.transform.scale(
            self.image,
            (max(1, round(TILESIZE * self.scale)),
             max(1, round(TILESIZE * self.scale))),
        )
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))


        self.x, self.y = x,y

        self.rect.x = self.x
        self.rect.y = self.y


    def update (self):
        pass

# Prolly change later, basic code for enemy projects.
class EnemyProjectile(Sprite):
    SCALE = 0.5

    def __init__(self,game,x,y ,angle,speed):

        self.game = game
        self.groups = game.all_sprites, game.projectiles
        Sprite.__init__(self, self.groups)

        self.scale = get_sprite_scale(self)
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE

        self.x = x
        self.y = y

        self.angle = math.radians(angle)
        self.speed = speed

        size = max(1, round(TILESIZE * self.scale))
        self.spritesheet = Spritesheet(path.join(self.game.img_dir,"Projectile1.png"))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image = scale_sprite_image(self.image, self.scale)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.hit_rect = self.rect

    def update(self):
        self.x += math.cos(self.angle) * self.speed * self.game.dt
        self.y += math.sin(self.angle) * self.speed * self.game.dt

        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.colliderect(self.game.player.hit_rect):
            self.hit()
        

    def hit(self):
        self.game.player.damage()
        self.kill()

# Game settings'
import pygame as pg

WIDTH = 800
HEIGHT = 800

TILESIZE = 32

FPS = 60

# Colors

WHITE = (255 , 255 , 255)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

# Player Settings

PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE - 5, TILESIZE - 5)
ENEMY_HIT_RECT = pg.Rect(0,0, TILESIZE - 5, TILESIZE - 5)

KEYBINDS = {
    "MoveUp" : pg.K_w,
    "MoveDown" : pg.K_s,
    "MoveLeft" : pg.K_a,
    "MoveRight" : pg.K_d,
}
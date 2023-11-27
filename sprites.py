import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *
from math import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

class Player(Sprite):
    def __init__(self, game, l_control, r_control, jump_control, img_file, x, y):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.img_file = img_file
        self.image = pg.image.load(os.path.join(img_folder, self.img_file)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.canmove = True
        self.l_control = l_control
        self.r_control = r_control
        self.jump_control = jump_control
        self.canjump = True
        self.times_jumped = 0
        self.cd = Cooldown()
        self.jump_cd = Cooldown()
        self.shield_cd = Cooldown()
        self.w_scale = 32
        self.h_scale = 32

    def controls(self):
        keys = pg.key.get_pressed()
        if self.canmove:
            if keys[pg.K_p]:
                print(self.game.paused)
                if self.game.paused:
                    self.game.paused = False
                else:
                    self.game.paused = True
            if keys[self.l_control]:
                self.acc.x = -5
                self.game.paused = False
            if keys[self.r_control]:
                self.acc.x = 5
            if keys[self.jump_control]:
                self.jump()

    def fire(self):
        mpos = pg.mouse.get_pos()
        print(mpos)
        targetx = mpos[0]
        targety = mpos[1]
        distance_x = targetx - self.rect.x
        distance_y = targety - self.rect.y
        angle = atan2(distance_y, distance_x)
        speed_x = 10 * cos(angle)
        speed_y = 10 * sin(angle)
        p = Pewpew(self.game, WIDTH/2, HEIGHT/2, 10, 10, speed_x, speed_y)
        self.game.all_sprites.add(p)
    
    def jump(self):
        print("i have jumped this many times " + str(self.times_jumped))
        if self.canjump and self.times_jumped < 2:
            self.acc.y = -PLAYER_JUMP
            self.times_jumped += 1
    def scale(self, x):
        self.image = pg.transform.scale(self.image, (floor(self.w_scale*x), floor(self.h_scale*x)))
    def update(self):
        self.shield_cd.ticking()
        self.jump_cd.ticking()
        self.cd.ticking()
        # print(self.shield_cd.delta)
        # print(self.jump_cd.delta)
        # this prevents players from moving through the left side of the platforms...
        phits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if self.vel[0] >= 0 and phits:
            if self.rect.right < phits[0].rect.left + 35:
                self.vel[0] = -self.vel[0]
                self.pos.x = phits[0].rect.left - 35
        self.rect = self.image.get_rect()
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # checks for mob hits
        # if you want to kill the mob when you collide change last argument to True
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        # if mob hits sets tagged to true
        if mhits:
            mhits[0].tagged = True
            mhits[0].cd.event_reset()
            mhits[0].image = pg.image.load(os.path.join(img_folder, "explode.png")).convert()
            mhits[0].image.set_colorkey(BLACK)
# platforms

class Pewpew(Sprite):
    def __init__(self, game, x, y, w, h, speed_x, speed_y):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.fired = False
    def update(self):
        hit = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # if (self.rect.y < 0 or self.rect.y > HEIGHT or self.rect.x < 0 or self.rect.x > WIDTH):
        #     self.kill()

class Platform(Sprite):
    def __init__(self, x, y, w, h, category, color):
        Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface((w, h))
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.category = category
        if self.category == "moving":
            self.tile_image = pg.image.load(os.path.join(img_folder, "plat_tile.png")).convert()
            self.speed = 5
        else:
            self.tile_image = pg.image.load(os.path.join(img_folder, "theBell.png")).convert()

    def update(self):
        self.image.blits([(self.tile_image, (0,0)), (self.tile_image, (16,0)), (self.tile_image, (32,0)), (self.tile_image, (48,0)), (self.tile_image, (64,0)), (self.tile_image, (80,0)),(self.tile_image, (96,0)),(self.tile_image, (0,0)),(self.tile_image, (112,0))])
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.bottomleft = self.pos
        if self.category == "moving":
            self.vel = vec(5,0)

class Powerup(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "health":
            self.speed = 5
    def update(self):
        pass

class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "enemy.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
        self.aggro_range = 300
        self.is_seeking = True
    def seeking(self, obj):
        if abs(self.rect.x - obj.rect.x) < self.aggro_range and abs(self.rect.y - obj.rect.y) < self.aggro_range:
            if self.rect.x < obj.rect.x:
                self.rect.x +=1
            if self.rect.x > obj.rect.x:
                self.rect.x -=1
            if self.rect.y < obj.rect.y:
                self.rect.y +=1
            if self.rect.y > obj.rect.y:
                self.rect.y -=1
    def update(self):
        if self.is_seeking:
            self.seeking(self.game.player)
            self.seeking(self.game.player2)
        self.cd.ticking()
        if self.cd.delta > 0.2 and self.tagged:
            self.kill()
        

# This file was created by: Chris Cozort
# Sources: Chris Bradfield game design

# Title: Skyrim gameloop simulator

# Overview: Create a top down 2d simulation of Skyrim's overall game loop

# Goals:





# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
from math import floor
import math

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.cd = Cooldown()
    
    def new(self):
        # add coin sound here
        self.coin_sound = pg.mixer.Sound(os.path.join(snd_folder, 'coin.mp3'))
        self.bgimage = pg.image.load(os.path.join(img_folder, "skyrim.png")).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_pews = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self, pg.K_a, pg.K_d, pg.K_w, "theBigBell.png", 300,  300)
        self.player2 = Player(self,pg.K_j, pg.K_l, pg.K_i, "theBell.png", 300, 300)
        # add instances to groups
        self.powerup = Powerup(50, 67, 32, 32, "jump")
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)
        
        # self.all_sprites.add(self.player2)
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)
        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        # this is where we create mobs...
        for m in range(0,5):
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events() 
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        self.cd.ticking()
        if self.player.health < 98:
            self.playing = False
        # handling collision in main instead of the mob or player class in sprites file
        mhits = pg.sprite.spritecollide(self.player, self.all_mobs, True)
        if mhits:
            self.player.health -= 1
            # play coin when collide with mob - which is weird because I don't have coins...
            self.coin_sound.play()
            self.player.scale(2)

        # if len(self.all_mobs) < 1:
        #     print("we are out of mobs!")
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH: 
            self.player.pos.x = 0
        
        # move plats up in group as you reach a point on screen
        # if self.player.pos.y < WIDTH/4:
        #     for p in self.all_platforms:
        #         p.rect.y += 25
        #         self.ground.rect.y += 25

        # this is what prevents the player from falling through the platform when falling down...
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        if hits:
            if hits[0].category == "moving":
                self.player.vel.x = hits[0].vel.x
            if self.player.vel.y > 0:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.times_jumped = 0
            elif self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y
            
        # checks to see if player collides specifically with the ground and sets him on top of it
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        if ghits:
            self.player.pos.y = self.ground.rect.top
            self.player.vel.y = 0
            self.player.times_jumped = 0
            if self.player.cd.delta == 2:
                self.player.cd.event_reset()
                self.player.health -= 1

        hits = pg.sprite.spritecollide(self.player2, self.all_platforms, False)
        if hits:
            if self.player2.vel.y > 0:
                self.player2.pos.y = hits[0].rect.top
                self.player2.vel.y = 0
        # prevent player from jumping through bottom of plat in future update...
        ghits = pg.sprite.collide_rect(self.player2, self.ground)
        if ghits:
            self.player2.pos.y = self.ground.rect.top
            self.player2.vel.y = 0

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                self.player.fire()
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            self.cd.event_reset()
        
    #################### Draw #############################
    def draw(self):
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bgimage, (0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("P1 - Health: " + str(self.player.health), 22, BLUE, WIDTH/2, HEIGHT/24)
        # self.draw_text("P2 - Health: " + str(self.player2.health), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.draw_text("acc: " + str(round(self.player.acc.y, 2)), 22, BLUE, 100, HEIGHT/6)
        self.draw_text("vel: " + str(round(self.player.vel.y, 2)), 22, BLUE, 100, HEIGHT/4)
        self.draw_text("cooldown: " + str(self.cd.delta), 22, BLUE, 200, HEIGHT/4)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BLACK)
        # self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("WASD to move", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        # self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        # if self.score > self.highscore:
        #     self.highscore = self.score
        #     self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            # with open(os.path.join(self.dir, HS_FILE), 'w') as f:
            #     f.write(str(self.score))
        # else:
        #     self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
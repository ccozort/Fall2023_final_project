# This file was created by: Chris Cozort
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

from random import randint
# game settings 
WIDTH = 800
HEIGHT = 500
FPS = 30

# player settings
PLAYER_JUMP = 10
PLAYER_GRAV = 1.5
global PLAYER_FRIC
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GROUND = (0, HEIGHT - 40, WIDTH, 40, "normal", (255, 0, 0))
PLATFORM_LIST = [
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 128, 16,"normal", (randint(0,255), randint(0,255), randint(0,255))),
                 (125, HEIGHT - 350, 128, 16, "moving", (255, 255, 255)),
                 (222, 200, 128, 16, "normal", (255, 255, 255)),
                 (222, 200, 128, 16, "normal", (255, 255, 255)),
                 (175, 100, 50, 16, "normal", (255, 255, 255) )]
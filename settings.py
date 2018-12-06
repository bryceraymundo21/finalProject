TITLE = "Cliff jumper"
# screen dims
WIDTH = 1000
HEIGHT = 600
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
SKY_BLUE = (143, 185, 252)
FONT_NAME = 'Comic Sans'
SPRITESHEET = "spritesheet_jumper.png"
SPRITESHEET2 = "spritesheet.png"
# data files
HS_FILE = "highscore.txt"
# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
# game settings
BOOST_POWER = 60
POW_SPAWN_PCT = 20
MOB_FREQ = 500
# layers - uses numerical value in layered sprites
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
LASER_LAYER = 3
CLOUD_LAYER = 0

# platform settings
''' old platforms from drawing rectangles'''
'''
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (65, HEIGHT - 300, WIDTH-400, 40),
                 (20, HEIGHT - 350, WIDTH-300, 40),
                 (200, HEIGHT - 150, WIDTH-350, 40),
                 (200, HEIGHT - 450, WIDTH-350, 40)]
'''
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (WIDTH/2, HEIGHT - 300),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 150),
                 (300, HEIGHT - 700),
                 (500, HEIGHT - 400),
                 (600, HEIGHT - 500),
                 (700, HEIGHT - 250),
                 (800, HEIGHT - 550),
                 (900, HEIGHT - 600),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 900),
                 (300, HEIGHT - 3500),
                 (500, HEIGHT - 100),
                 (600, HEIGHT - 205),
                 (600, HEIGHT - 400),
                 (800, HEIGHT - 600),
                 (900, HEIGHT - 500)]

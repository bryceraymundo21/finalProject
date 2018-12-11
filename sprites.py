# sprite classes for game
# i used some ideas from CodePylet https://www.youtube.com/watch?v=osDofIdja6s&t=1038s
# i also borrowed pretty much all of this from kids can code - thanks!
# on acceleration https://www.khanacademy.org/science/physics/one-dimensional-motion/kinematic-formulas/v/average-velocity-for-constant-acceleration 
# on vectors: https://www.youtube.com/watch?v=ml4NSzCQobk 


import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint, randrange, choice
from settings import *
import math

vec = pg.math.Vector2
class Spritesheet:
    # class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
class Player(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group - thanks pygame!
        self._layer = PLAYER_LAYER
        # add player to game groups when instantiated
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.doubleJumpPower = False
        self.laserPower = False
        self.laser = None
        # self.image = pg.Surface((30,40))
        # self.image = self.game.spritesheet.get_image(614,1063,120,191)
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
     
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(690, 406, 120, 201),
                                self.game.spritesheet.get_image(614, 1063, 120, 191)
                                ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                                self.game.spritesheet.get_image(692, 1458, 120, 207)
                                ]
        '''setup left frames by flipping and appending them into an empty list'''
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)
    # def getLaser(self):
    #     #add laser
    #     self.laser = Laser(self,self.player)
    # def updateLaser(self,game):
    #     self.laser.update()

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x =  -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        # set player friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # jump to other side of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
    # cuts the jump short when the space bar is released
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def jump(self):
        # check pixel below
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # adjust based on checked pixel
        self.rect.y -= 2
        # only allow jumping if player is on platform
        if hits and self.doubleJumpPower== False and not self.jumping:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell the program that player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
       
        #can jump as many times you want for a limited time
        if self.doubleJumpPower == True:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell the program that player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
           
    def animate(self):
        # gets time in miliseconds
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                '''
                assigns current frame based on the next frame and the remaining frames in the list.
                If current frame is 'two' in a list with three elements, then:
                2 + 1 = 3; 3 modulus 3 is zero, setting the animation back to its first frame.
                If current frame is zero, then:
                0 + 1 = 1; 1 modulus 3 is 1; 2 modulus 3 is 2; 3 modulus 3 is o

                '''
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # checks state
        if not self.jumping and not self.walking:
            # gets current delta time and checks against 200 miliseconds
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                # reset bottom for each frame of animation
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # collide will find this property if it is called self.mask
        self.mask = pg.mask.from_surface(self.image)

class Laser(Sprite):
    def __init__(self, game, player):
        # allows layering in LayeredUpdates sprite group
        self._layer = LASER_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image = pg.Surface((50,600))
        self.rotated_image = self.image
        self.original_image = self.image
        self.image.fill(REDDISH)
        self.rect = self.image.get_rect()
        self.rotated_rect = self.rect
        self.original_rect = self.rect
        self.rect.centerx = self.player.rect.centerx
        self.rect.bottom = self.player.rect.top - 5
    def update(self):
        self.rect.bottom = self.player.rect.top - 5
        # makes the x and y the same as the player
        self.rect.x = self.player.pos.x
        self.rect.y = self.player.pos.y

        

        # # Calculate x and y distances to the mouse pos.
        # run, rise = (mouse_pos[0]-x, mouse_pos[1]-y)
        # # Pass the rise and run to atan2 (in this order)
        # # and convert the angle to degrees.
        # angle = math.degrees(math.atan2(rise, run))
        # # Rotate the image (use the negative angle).
        # rotimage = pygame.transform.rotate(image, -angle)
        # rect = rotimage.get_rect(center=(x, y))
        # return rotimage, rect
        # mouse_x, mouse_y = pg.mouse.get_pos()
        # rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        # self.newImage = pg.transform.rotate(self.image, int(angle))
        # self.rect = self.image.get_rect(center=self.position)

class LeftWing(Sprite):
    def __init__(self, game, player):
        # allows layering in LayeredUpdates sprite group
        self._layer = LASER_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.left_wing = self.game.spritesheet.get_image(558, 651, 85, 74)
        self.right_wing = self.game.spritesheet.get_image(571, 1458, 85,74)
        self.image = self.left_wing
        self.rect = self.image.get_rect()

        self.rect.centerx = self.player.rect.centerx
        self.rect.bottom = self.player.rect.top - 5
    def update(self):
        self.rect.bottom = self.player.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        self.rect.x = self.player.pos.x
        self.rect.y = self.player.pos.y

class Cloud(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = CLOUD_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.clouds
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange (50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), 
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        self.speed = randrange(1,3)
    def update(self):
        if self.rect.top > HEIGHT * 2: 
            self.kill
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width
class Platform(Sprite):
    def __init__(self, game, zone, x, y):
        # allows layering in LayeredUpdates sprite group
        self._layer = PLATFORM_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        
        imageCake = [self.game.spritesheet.get_image(0, 576,380, 94),
	                self.game.spritesheet.get_image(0, 0, 380, 94),
	                self.game.spritesheet.get_image(218, 1456, 201, 100),
	                self.game.spritesheet.get_image(262,1152,200,100)]
        imageGrass = [self.game.spritesheet.get_image(0, 288, 380, 94), 
                    self.game.spritesheet.get_image(213, 1662, 201, 100)]
        imageWood = [self.game.spritesheet.get_image(0,960,380,94),
                    self.game.spritesheet.get_image(218, 1558, 200,100)]
        imageStone = [self.game.spritesheet.get_image(0,96,380,94),
                    self.game.spritesheet.get_image(382,408, 200, 100)]
        imageSnow = [self.game.spritesheet.get_image(0,768,380,94),
                    self.game.spritesheet.get_image(213,1764,201,100)]
        if zone =="grass":
            self.image = random.choice(imageGrass)
        if zone =="cake":
            self.image = random.choice(imageCake)
        if zone == "wood":
            self.image = random.choice(imageWood)
        if zone == "stone":
            self.image = random.choice(imageStone)
        if zone == "snow":
            self.image = random.choice(imageSnow)
        self.image.set_colorkey(BLACK)
        '''leftovers from random rectangles before images'''
        # self.image = pg.Surface((w,h))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)
class Pow(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = POW_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost','doubleJump','laser'])
        if self.type == 'boost':
            self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        if self.type == 'doubleJump':
            self.image = self.game.spritesheet.get_image(826, 1292, 71, 70)
        if self.type == 'laser':
            self.image = self.game.spritesheet.get_image(826,134,71,70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT//1.5)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 3 or  self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

# this file was created by Bryce Raymundo
# Sources: goo.gl/2KMivS https://bit.ly/2Eiqmtx shooting carrots from Benthan, following mouse from Joe
# now available in github

'''
**********Gameplay ideas:
*means its done or close to being done
*Jump on enemy head to create jump boost using power up code
Platforms move back and forth-Did not get to this feature
Add a death screen-Did not get to this feature
*Increase screen size
*Change the platform theme based on score
*Shoot carrots using x to kill enemies  

**********Bugs
when you get launched by powerup or head jump player sometimes snaps to platform abruptly 
happens when hitting jump during power up boost
*the double jump lasts forever instead of 10 seconds

**********Gameplay fixes
Platform randomness leaves player in limbo for extended periods
Lower spawn location so player can get out of random stuck situations
 

**********Features
*Varied powerups
*Double jump
*Shooting laser beams to destroy enemies
*Roblox oof sound plays when you kill an enemy
*Equip sound for laser


'''
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from math import *

class Game():
    def __init__(self):
        #init game window
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.start_ticks=pg.time.get_ticks()
        self.mobTimes = 4000
        print(self.start_ticks)
    def load_data(self):
        #print("load data is called...")
        # sets up directory name
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # opens file with write options
        ''' with is a contextual option that handles both opening and closing of files to avoid
        issues with forgetting to close
        '''
        try:
            # changed to r to avoid overwriting error
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                #print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                #print("exception")
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET)) 
        #load cloud images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # load sounds
        # great place for creating sounds: https://www.bfxr.net/
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))
        self.head_jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump39.wav'))
        self.laser_sound = pg.mixer.Sound(path.join(self.snd_dir, 'laser.wav'))
        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'rabloxDeath.wav'))
    def new(self):
        self.zone = "grass"
        self.zoneRotation=0
        self.changeInScore = 2000
        self.score = 0
        self.carrot_pow=0
        # add all sprites to the pg group
        # below no longer needed - using LayeredUpdate group
        # self.all_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create platforms group
        self.platforms = pg.sprite.Group()
        # create clouds group
        self.clouds = pg.sprite.Group()
        # add powerups
        self.powerups = pg.sprite.Group()
        self.mob_timer = 0
        #add carrots
        self.carrotups = pg.sprite.Group()
        # add a player 1 to the group
        self.player = Player(self)
        
        self.lasers = pg.sprite.Group()
        # add mobs
        self.mobs = pg.sprite.Group()
        
        # no longer needed after passing self.groups in Sprites library file
        # self.all_sprites.add(self.player)
        # instantiate new platform 
        for plat in PLATFORM_LIST:
            # no longer need to assign to variable because we're passing self.groups in Sprite library
            # p = Platform(self, *plat)
            Platform(self, self.zone, *plat)
            # no longer needed because we pass in Sprite lib file
            # self.all_sprites.add(p)
            # self.platforms.add(p)
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        # load music
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        # call the run method
        self.run()
    def run(self):
        # game loop
        # play music
        pg.mixer.music.play(loops=-1)
        # set boolean playing to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
    
    def update(self):
        #changes how the platforms look based on the score
        if self.changeInScore < self.score:
            self.changeInScore = self.score + 1000
            print(self.changeInScore)
            self.zoneRotation +=1
            if self.zoneRotation == 0:
                self.zone = "grass"
            if self.zoneRotation == 1:
                self.zone = "wood"
            if self.zoneRotation == 2:
                self.zone = "cake"
            if self.zoneRotation == 3:
                self.zone = "stone"
            if self.zoneRotation == 4:
                self.zone = "snow"
            if self.zoneRotation >= 5:
                self.zoneRotation= 0
                self.zone="grass"

        if pg.sprite.groupcollide(self.mobs, self.carrotups, True, True):
            self.death_sound.play()
            self.score +=10
    


        self.all_sprites .update()
        
        # shall we spawn a mob  ?
        now = pg.time.get_ticks()
        if now - self.mob_timer > self.mobTimes + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        ##### check for mob collisions ######
        # now using collision mask to determine collisions
        # can use rectangle collisions here first if we encounter performance issues
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            # can use mask collide here if mob count gets too high and creates performance issues
            if self.player.pos.y - 35 < mob_hits[0].rect_top:
                self.head_jump_sound.play()
                self.player.vel.y = -BOOST_POWER
            else:
                self.playing = False

        # check to see if player can jump - if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # set var to be current hit in list to find which to 'pop' to when two or more collide with player
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        #print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit
                # fall if center is off platform
                if self.player.pos.x < find_lowest.rect.right + 10 and self.player.pos.x > find_lowest.rect.left - 10:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                
        # if player reaches top 1/4 of screen...
        if self.player.rect.top <= HEIGHT / 4:
            # spawn a cloud
            if randrange(100) < 13:
                Cloud(self)
            # set player location based on velocity
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / randrange(2,10)), 2)
            # creates slight scroll at the top based on player y velocity
            # scroll plats with player
            
            for mob in self.mobs:
                # creates slight scroll based on player y velocity
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                # creates slight scroll based on player y velocity
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT + 40:
                    plat.kill()
                    self.score += 10
        # if player hits a power up
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
            #added double jump
            if pow.type == 'doubleJump':
                #Player(self.doubleJump = True)
                self.boost_sound.play()
                self.player.doubleJumpPower=True
                self.jetpack= Jetpack(self,self.player)

            #if the power type is a laser
            if pow.type == 'laser':
                self.laser_sound.play()
                self.mobTimes = 500
                self.player.laserPower=True
                #add laser
                self.laser = Laser(self,self.player)
            
            #if the player hits the catus reduce score by 100
            if pow.type == 'decor':
                self.score = self.score-100
                
                self.draw_text("-100",100, WHITE, self.player.pos.x, self.player.pos.y)

                
        #if the player aquired double jump run this for 5 seconds
        if self.player.doubleJumpPower==True:
            #adds a timer
            self.seconds=(pg.time.get_ticks()-self.start_ticks)/1000
            
            #rounds to seconds
            self.intsecs = int(round(self.seconds))

            if self.seconds > 5:
                #destroys the jetpack
                self.jetpack.kill()
                self.player.doubleJumpPower=False
                self.start_ticks=pg.time.get_ticks() 
                self.jetpack.kill()
                
                

        #if the player acquired laser run this for 10 seconds
        if self.player.laserPower==True:
            self.seconds=(pg.time.get_ticks()-self.start_ticks)/1000
            self.intsecs = int(round(self.seconds))
            #if the laser collides with a mob destroy both of them
            if pg.sprite.groupcollide(self.mobs, self.lasers, True, False):
                self.death_sound.play()
                self.score +=10

            #sets the mob timer back to normal aft er 5 seconds            
            if self.seconds > 5:
                self.mobTimes = 4000

            #after 5 seconds kill the laser                
            if self.seconds > 10:
                
                self.laser.kill()
                self.player.laserPower=False
                self.start_ticks=pg.time.get_ticks() 
                self.laser.kill()
                


        # Die!
        if self.player.rect.bottom > HEIGHT:
            '''make all sprites fall up when player falls'''
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                '''get rid of sprites as they fall up'''
                if sprite.rect.bottom < -25:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        # generate new random platforms
        while len(self.platforms) < 20:
            width = random.randrange(50, 950)
            ''' removed widths and height params to allow for sprites '''
            """ changed due to passing into groups through sprites lib file """
            # p = Platform(self, random.randrange(0,WIDTH-width), 
            #                 random.randrange(-75, -30))
            
            Platform(self, self.zone, random.randrange(0,WIDTH-width),
                            random.randrange(-75, -30))
            # self.platforms.add(p)
            # self.all_sprites.add(p)
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        """ # cuts the jump short if the space bar is released """
                        self.player.jump_cut()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        Carrot(self,self.player.rect.centerx, self.player.rect.centery)
                        self.carrotups.update()
    def draw(self):
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        """ # not needed now that we're using LayeredUpdates """
        # self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        #adds a timer to the bottom of the player sprite
        if self.player.doubleJumpPower==True:
            self.draw_text(str(self.intsecs), 100, WHITE, self.player.pos.x, self.player.pos.y)
        if self.player.laserPower == True:
            self.draw_text(str(self.intsecs), 100, WHITE, self.player.pos.x, self.player.pos.y)
        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()
    def wait_for_key(self): 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
    # def is_collided_with(self, sprite):
    #     return self.rect.colliderect(sprite.rect)

    def show_start_screen(self):
        """ # game splash screen """
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        """ # game splash screen """
        if not self.running: 
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 60)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)


        pg.display.flip()
        self.wait_for_key()
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")
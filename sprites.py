# This code was created by: Ian Na

# Importing modules
from settings import *
import pygame as pg
from pygame.sprite import Sprite
import random
import time
import threading
from os import path

#animated sprite stuff
dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

#referenced ChatGPT
def countdown_timer(seconds, self):
    while seconds:
        time.sleep(1)
        seconds -= 1
        print(self.tptimer)
    self.tptimer = 1

def wish_timer(seconds, self):
    while seconds:
        time.sleep(0.25)
        seconds -= 1
        print(self.wishtimer)
    self.wishtimer = 1

def shop_timer(seconds, self):
    while seconds:
        time.sleep(0.25)
        seconds -= 1
        print(self.shoptimer)
    self.shoptimer = 1

def wish_shop_timer(seconds, self):
    while seconds:
        time.sleep(0.25)
        seconds -= 1
        print(self.wishshoptimer)
    self.wishshoptimer = 1

def wish_inv_timer(seconds, self):
    while seconds:
        time.sleep(1)
        seconds -= 1
        print(self.wishshoptimer)
    self.wishinvtimer = 1
    self.inv = False

def trap_inv_timer(seconds, self):
    while seconds:
        time.sleep(100)
        seconds -= 1
        print(self.trapinvtimer)
    self.trapinvtimer = 1

# Coach Cozort's Code
# sets up file with multiple images...
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

wish = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
SPRITESHEET = "ROFL.png"

# Create a player class
class Player(Sprite):
    # Initializing the player class with attributes.
    def __init__(self, game, x, y): # game parameter = self o/Game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
    # start animated sprite code
        self.load_images()
        self.image = self.standing_frames[0]
        self.jumping = False
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.jumping = False
        self.walking = False
        self.material = True
    # end animated sprite code
        #letting the sprite use stuff in game (in main.py)
        self.game = game
        # properties of the character
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.lives = 100
        self.score = 0
        self.inv = False
        self.ptw = False
        self.powertime = 1
        self.primegem = 1
        self.tptimer = 1
        self.wishtimer = 1
        self.wishinvtimer = 1
        self.items = 0
        self.shop1 = 0
        self.shop = 0
        self.trap = "ACTIVE"
        self.win = "NO"
        self.trapinvtimer = 1
        self.shoptimer = 1
        self.pulls = 0
        self.wishshoptimer = 1
        self.clock = pg.time.Clock()
    
    #A pygame-specific thing, this lets you detect the key pressed 
    def get_keys(self):
        global PULLS
        global SHOP
        self.vx, self.vy  = 0, 0  
        keys = pg.key.get_pressed()

        if keys[pg.K_5] and self.shoptimer == 1:
            self.shop1 += 1
            #chatgpt referenced for odd/even verification
            if self.shop1 % 2 == 0:
                self.shop = 0
            else:
                self.shop = 1
            self.shoptimer -= 1
            timer_thread = threading.Thread(target=shop_timer, args=(1, self))
            timer_thread.start()            
        if self.shop == 1:
            if keys[pg.K_1] and self.primegem > 160 and self.wishshoptimer == 1:
                PULLS += 1
                self.pulls += 1
                self.primegem -= 160
                self.items += 1
                print('this is a shop item purchase. thanks')
                print (str(PULLS))
                self.wishshoptimer -= 1
                timer_thread = threading.Thread(target=wish_shop_timer, args=(1, self))
                timer_thread.start()
            if keys[pg.K_2] and self.primegem > 600 and self.wishinvtimer == 1:
                self.items += 1
                self.wishinvtimer = 0
                self.inv = True
                self.primegem -= 600
                timer_thread = threading.Thread(target=wish_inv_timer, args=(10, self))
                timer_thread.start()
            if keys[pg.K_3] and self.primegem > 1000 and self.trapinvtimer == 1:
                self.items += 1
                self.trapinvtimer = 0
                self.trap = "DISARMED"
                self.primegem -= 1000
                timer_thread = threading.Thread(target=trap_inv_timer, args=(10, self))
                timer_thread.start()
            if keys[pg.K_4]:
                self.items += 1
            if keys[pg.K_i] and keys[pg.K_a] and keys[pg.K_n]:
                self.primegem += 100000

        if SHOP == 0:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                if self.tptimer == 1:
                    self.vx = -PLAYER_SPEED - (self.score * 10)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                if self.tptimer == 1:
                    self.vx = PLAYER_SPEED + (self.score * 10)
            if keys[pg.K_UP] or keys[pg.K_w]:
                if self.tptimer == 1:
                    self.vy = -PLAYER_SPEED - (self.score * 10)
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                if self.tptimer == 1:
                    self.vy = PLAYER_SPEED + (self.score * 10)
            if keys[pg.K_i] and keys[pg.K_a] and keys[pg.K_n]:
                self.primegem += 100000

        if self.vx != 0 and self.vy != 0:
            # sqrt(2)/2
            self.vx *= 0.7071
            self.vy *= 0.7071
            # in order to reduce diagonal speed
        now = pg.time.get_ticks()
        if keys[pg.K_SPACE] and PULLS > 0 and self.wishtimer > 0:
            PULLS -= 1
            self.pulls -= 1
            self.wishtimer -= 1
            timer_thread = threading.Thread(target=wish_timer, args=(1, self))
            timer_thread.start()
            print (str(PULLS))
            randompull = random.choice(wish)
            print ("result" + str(randompull))
            if randompull == 20:
                self.ptw = True
                self.win = "YES"
                self.image.fill(D_RED)
                print("you won")

    #Essentially detects walls on both axes, then stops the velocity in that direction
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0 and self.ptw == False:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0 and self.ptw == False:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0 and self.ptw == False:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0 and self.ptw == False:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    #rapidly decreases HP based on collision with an enemy
    def collide_with_enemies(self,kill):
        hits = pg.sprite.spritecollide(self, self.game.enemies, kill)
        if hits and self.inv == False and self.ptw == False:
            self.lives -=2 #a very short forgiveness window between player enemy contact and player death
            print(self.lives)
            return True
        
#Coach Cozort's Code Referenced, this detects each class the player collides with
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.score += 1
                self.primegem += 60
            elif str(hits[0].__class__.__name__) == "WallTP" and self.ptw == False and self.trap == "ACTIVE":
                if self.tptimer > 0:
                    self.tptimer -= 1
                timer_thread = threading.Thread(target=countdown_timer, args=(3, self))
                timer_thread.start()
#start animated sprite code    
#this sets the boundaries for the frame fropm the spritesheet
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
                              self.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
        self.jump_frame.set_colorkey(BLACK)
#this is the loop that runs on update, which changefs the frame when a certain time has passed
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
#end animated sprite code

    #continuous detection of these states
    def update(self):
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.tptimer == 0:
            self.rect.x = (0)
            self.rect.y = (0)
        else:
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
        if self.collide_with_enemies(False):
            if self.lives == 0:
                self.game.player.kill()
                print('you died')
#Coach Cozort's Code
        self.collide_with_group(self.game.coins,True)
        self.collide_with_group(self.game.walltp,True)    

# Create a wall class
class Wall(Sprite):
    # Initializing the wall class with attributes.
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        # create a square
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Shop(Sprite):
    # Initializing the wall class with attributes.
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.shop
        Sprite.__init__(self, self.groups)
        self.game = game
        # create a square
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.items = 0

#add something here for mouse input, and then it will change shop variable to 1 and start all the other things.
#purchase: wishes, 

    def get_keys1(self):
        global SHOP
        global PULLS
        keys = pg.key.get_pressed()
        if keys[pg.K_5]:
            SHOP = 1
        if SHOP == 1:
            if keys[pg.K_1]:
                PULLS += 1
                self.items += 1
                print('this is a shop item purchase. thanks')
                print (str(PULLS))
            if keys[pg.K_2]:
                self.items += 1 
            if keys[pg.K_3]:
                self.items += 1
            if keys[pg.K_4]:
                self.items += 1

    def update(self):
        global SHOP
        self.get_keys1()
        if self.items == 5:
            SHOP = 0

# Create a start block class, like walls
class StartBlock(Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.starts
        Sprite.__init__(self, self.groups)
        self.game = game
        # create a square
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#same code as the Startblock, basically the simple color, group, and dimensions
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y        
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #same as the enemy/player classes, but very stripped down.

# this is the class for the trap, like coins.
class WallTP(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walltp
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y        
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#We made a basic enemy as a group
class Enemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game # The player can access the game class
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, 0
 
    #detects a collision with wall sprite
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vx *= -1 #this is the source of the left and right movement
            self.rect.x = self.x

    #continuously called, this changes player position and calls the check collision code
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls() #continous polling of this collision right above
        self.rect.y = self.y

#Same as the normal enemy but vertical movement, and is slower to balance the game
class Vertenemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game # The player can access the game class
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, ENEMY_SPEED/1.5

    #same code as the player sprite, detects wall collision
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vy *= -1 #this is the source of the left and right movement
            self.rect.y = self.y

    #Continuously called, changes enemy position and runs detect wall collision code
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # self.x += self.vx * self.game.dt/rot
        # self.y += self.vy * self.game.dt/rot
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_walls() #continous polling of this collision right above
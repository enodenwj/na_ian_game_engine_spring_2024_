# This code was created by: Ian Na

# Importing modules
from settings import *
import pygame as pg
from pygame.sprite import Sprite

# Create a player class
class Player(Sprite):
    # Initializing the player class with attributes.
    def __init__(self, game, x, y): # game parameter = self o/Game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
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
    
    #A pygame-specific thing, this lets you detect the key pressed 
    def get_keys(self):
        self.vx, self.vy  = 0, 0  
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED - (self.score * 10)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED + (self.score * 10)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED - (self.score * 10)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED + (self.score * 10)
        # in order to reduce diagonal speed
        if self.vx != 0 and self.vy != 0:
            # sqrt(2)/2
            self.vx *= 0.7071
            self.vy *= 0.7071

    #Essentially detects walls on both axes, then stops the velocity in that direction
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    #rapidly decreases HP based on collision with an enemy
    def collide_with_enemies(self,kill):
        hits = pg.sprite.spritecollide(self, self.game.enemies, kill)
        if hits:
            self.lives -=2 #a very short forgiveness window between player enemy contact and player death
            print(self.lives)
            return True
#Coach Cozort's Code
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.score += 1
#               self.game.cooldown.cd = 5

    #continuous detection of these states
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.collide_with_enemies(False):
            if self.lives == 0:
                self.game.player.kill()
                print('you died')
#Coach Cozort's Code
        self.collide_with_group(self.game.coins, True)
            
#        if self.game.cooldown.cd < 1:
#            self.cooling = False

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

# Create a start block class
class StartBlock(Sprite):
    # Initializing the wall class with attributes.
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
 
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vx *= -1 #this is the source of the left and right movement
            self.rect.x = self.x

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls() #continous polling of this collision right above
        self.rect.y = self.y

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
 
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vy *= -1 #this is the source of the left and right movement
            self.rect.y = self.y

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_walls() #continous polling of this collision right above
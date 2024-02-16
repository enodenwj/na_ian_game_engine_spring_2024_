#This file was created by: Ian Na

#importing libraries including our own
import pygame as pg
import sys
from settings import * #wildcard symbol (meaning import all)
from sprites import *
from random import randint # a random integer in a specified range
from os import path

#creating the class
class Game:
    #initializing the class, with its attributes
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) 
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,  100) # delays the input
        self.load_data()
        self.running = True

    # loading save game data and other things
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt',) as f:
            for line in f:
                self.map_data.append(line)

    # initializing all variables and setting up groups and instantiating classes
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        #self.player = Player(self, 10, 10)
        #for x in range(10, 20):
        #    Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            #print(row)
            #print(tiles)
            for col, tile in enumerate(tiles):
                #print(col)
                #print(tiles)
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "E":
                    self.enemy = Enemy(self,col,row)
                    
    #we have defined the run method in the game engine
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            # input process output

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        # single line updates all

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # essentially all inputs we give 
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=+1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

#I have instantiated the game
g = Game()
#g.show_start_screen()
while True:
    g.new()
    g.run()
    #g.show_go_screen()

#    #input method (move into future player class)
#    def input(self):
#        keys = pg.key.get_pressed()
#        if keys[pg.K_LEFT]:
#            print("I HIT THE LEFT ARROW")
#        if keys[pg.K_RIGHT]:
#            print("I HIT THE RIGHT ARROW")

#        #the ==True is implied
#        while self.running:
#            for event in pg.event.get():
#                if event.type == pg.QUIT:
#                    self.running = False
#            self.input()
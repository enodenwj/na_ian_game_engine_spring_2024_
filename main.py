#This file was created by: Ian Na

#Game design goals: timer, enemy, start/end screen, gamble, movement trap, animated sprite(done)

#Freedom: true, x,y movement
#Goals: Eat all the coins to trigger game over
#Rules: Walls stop the player, enemies kill the player (very minimal hitpoints, almost instant death)
#Feedback: The hitpoints, player speed are shown in game, and other statuses

#final goal: shop for buffs and gambling... paypal link
#make something like the startscreen but for a shop, then stop updating game when you clock on a sprite that will be the button to open shop
#shop closes after you buy 5 items you can buy 5 and only 5 items.
#items will be binded to keys, so the code can easily just exist all in the sprite that will be the button to open shop.

#importing libraries including our own
import pygame as pg
import sys
from settings import * #wildcard symbol (meaning import all)
from sprites import *
from random import randint # a random integer in a specified range
from os import path
import time

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
        self.timer=90
#        self.game_paused = True

    # loading save game data and other things
    def load_data(self):
        game_folder = path.dirname(__file__)
        #self.img_folder = path.join(self.game_folder, 'images')
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt',) as f:
            for line in f:
                self.map_data.append(line)

    #Coach Cozort's Code referenced
    def show_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('Courier New')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    #Prints the start screen
    def display_end_screen(self):
        self.screen.fill(STARTBG)
        x = WIDTH/2
        y = HEIGHT/4
        factor = 15 # factor added for easy modification
        self.show_text(self.screen, "          _____                    _____           _______                   _____                    _____                    _____", 10, YELLOW, x, y+factor )
        self.show_text(self.screen, "         /\    \                  /\    \         /::\    \                 /\    \                  /\    \                  /\    \\", 10, YELLOW, x, y + 2*factor)
        self.show_text(self.screen, "        /::\    \                /::\____\       /::::\    \               /::\    \                /::\____\                /::\    \\", 10, YELLOW, x, y + 3*factor)
        self.show_text(self.screen, "       /::::\    \              /:::/    /      /::::::\    \             /::::\    \              /:::/    /               /::::\    \\", 10, YELLOW, x, y + 4*factor)
        self.show_text(self.screen, "      /::::::\    \            /:::/    /      /::::::::\    \           /::::::\    \            /:::/    /               /::::::\    \\", 10, YELLOW, x, y + 5*factor)
        self.show_text(self.screen, "     /:::/\:::\    \          /:::/    /      /:::/~~\:::\    \         /:::/\:::\    \          /:::/    /               /:::/\:::\    \\", 10, YELLOW, x, y + 6*factor)
        self.show_text(self.screen, "    /:::/__\:::\    \        /:::/    /      /:::/    \:::\    \       /:::/  \:::\    \        /:::/____/               /:::/__\:::\    \\", 10, YELLOW, x, y + 7*factor)
        self.show_text(self.screen, "   /::::\   \:::\    \      /:::/    /      /:::/    / \:::\    \     /:::/    \:::\    \      /::::\    \               \:::\   \:::\    \\", 10, YELLOW, x, y + 8*factor)
        self.show_text(self.screen, "  /::::::\   \:::\    \    /:::/    /      /:::/____/   \:::\____\   /:::/    / \:::\    \    /::::::\____\________    ___\:::\   \:::\    \\", 10, YELLOW, x+5, y + 8*factor)
        self.show_text(self.screen, " /:::/\:::\   \:::\ ___\  /:::/    /      |:::|    |     |:::|    | /:::/    /   \:::\    \  /:::/\:::::::::::\    \  /\   \:::\   \:::\    \\", 10, YELLOW, x+5, y + 9*factor) 
        self.show_text(self.screen, "/:::/__\:::\   \:::|    |/:::/____/       |:::|____|     |:::|    |/:::/____/     \:::\____\/:::/  |:::::::::::\____\/::\   \:::\   \:::\____\\", 10, YELLOW, x+5, y + 10*factor)
        self.show_text(self.screen, "\:::\   \:::\  /:::|____|\:::\    \        \:::\    \   /:::/    / \:::\    \      \::/    /\::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /", 10, YELLOW, x, y + 11*factor)
        self.show_text(self.screen, " \:::\   \:::\/:::/    /  \:::\    \        \:::\    \ /:::/    /   \:::\    \      \/____/  \/____|::|   |           \:::\   \:::\   \/____/", 10, YELLOW, x, y + 12*factor)
        self.show_text(self.screen, "  \:::\   \::::::/    /    \:::\    \        \:::\    /:::/    /     \:::\    \                    |::|   |            \:::\   \:::\    \\", 10, YELLOW, x-10, y + 13*factor)     
        self.show_text(self.screen, "   \:::\   \::::/    /      \:::\    \        \:::\__/:::/    /       \:::\    \                   |::|   |             \:::\   \:::\____\\", 10, YELLOW, x, y + 14*factor)    
        self.show_text(self.screen, "    \:::\  /:::/    /        \:::\    \        \::::::::/    /         \:::\    \                  |::|   |              \:::\  /:::/    /", 10, YELLOW, x, y + 15*factor)    
        self.show_text(self.screen, "     \:::\/:::/    /          \:::\    \        \::::::/    /           \:::\    \                 |::|   |               \:::\/:::/    /", 10, YELLOW, x, y + 16*factor)     
        self.show_text(self.screen, "      \::::::/    /            \:::\    \        \::::/    /             \:::\    \                |::|   |                \::::::/    /", 10, YELLOW, x, y + 17*factor)      
        self.show_text(self.screen, "       \::::/    /              \:::\____\        \::/____/               \:::\____\               \::|   |                 \::::/    /", 10, YELLOW, x, y + 18*factor)       
        self.show_text(self.screen, "        \::/____/                \::/    /         ~~                      \::/    /                \:|   |                  \::/    /", 10, YELLOW, x, y + 19*factor)        
        self.show_text(self.screen, "         ~~                       \/____/                                   \/____/                  \|___|                   \/____/", 10, YELLOW, x, y + 20*factor)
        self.show_text(self.screen, "GAME OVER", 50, GREEN, x+20, y + 23*factor)
        self.show_text(self.screen, "THIS GAME WILL CLOSE IN 5 SECONDS", 20, GREEN, x+20, y + 27*factor)
        pg.display.flip()

    #Longer way of inserting every line of the start screen directly into main
    def display_startup_screen(self):
        self.screen.fill(STARTBG)
        x = WIDTH/2
        y = HEIGHT/4
        factor = 15
        self.show_text(self.screen, "          _____                    _____           _______                   _____                    _____                    _____", 10, YELLOW, x, y+factor )
        self.show_text(self.screen, "         /\    \                  /\    \         /::\    \                 /\    \                  /\    \                  /\    \\", 10, YELLOW, x, y + 2*factor)
        self.show_text(self.screen, "        /::\    \                /::\____\       /::::\    \               /::\    \                /::\____\                /::\    \\", 10, YELLOW, x, y + 3*factor)
        self.show_text(self.screen, "       /::::\    \              /:::/    /      /::::::\    \             /::::\    \              /:::/    /               /::::\    \\", 10, YELLOW, x, y + 4*factor)
        self.show_text(self.screen, "      /::::::\    \            /:::/    /      /::::::::\    \           /::::::\    \            /:::/    /               /::::::\    \\", 10, YELLOW, x, y + 5*factor)
        self.show_text(self.screen, "     /:::/\:::\    \          /:::/    /      /:::/~~\:::\    \         /:::/\:::\    \          /:::/    /               /:::/\:::\    \\", 10, YELLOW, x, y + 6*factor)
        self.show_text(self.screen, "    /:::/__\:::\    \        /:::/    /      /:::/    \:::\    \       /:::/  \:::\    \        /:::/____/               /:::/__\:::\    \\", 10, YELLOW, x, y + 7*factor)
        self.show_text(self.screen, "   /::::\   \:::\    \      /:::/    /      /:::/    / \:::\    \     /:::/    \:::\    \      /::::\    \               \:::\   \:::\    \\", 10, YELLOW, x, y + 8*factor)
        self.show_text(self.screen, "  /::::::\   \:::\    \    /:::/    /      /:::/____/   \:::\____\   /:::/    / \:::\    \    /::::::\____\________    ___\:::\   \:::\    \\", 10, YELLOW, x+5, y + 8*factor)
        self.show_text(self.screen, " /:::/\:::\   \:::\ ___\  /:::/    /      |:::|    |     |:::|    | /:::/    /   \:::\    \  /:::/\:::::::::::\    \  /\   \:::\   \:::\    \\", 10, YELLOW, x+5, y + 9*factor) 
        self.show_text(self.screen, "/:::/__\:::\   \:::|    |/:::/____/       |:::|____|     |:::|    |/:::/____/     \:::\____\/:::/  |:::::::::::\____\/::\   \:::\   \:::\____\\", 10, YELLOW, x+5, y + 10*factor)
        self.show_text(self.screen, "\:::\   \:::\  /:::|____|\:::\    \        \:::\    \   /:::/    / \:::\    \      \::/    /\::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /", 10, YELLOW, x, y + 11*factor)
        self.show_text(self.screen, " \:::\   \:::\/:::/    /  \:::\    \        \:::\    \ /:::/    /   \:::\    \      \/____/  \/____|::|   |           \:::\   \:::\   \/____/", 10, YELLOW, x, y + 12*factor)
        self.show_text(self.screen, "  \:::\   \::::::/    /    \:::\    \        \:::\    /:::/    /     \:::\    \                    |::|   |            \:::\   \:::\    \\", 10, YELLOW, x-10, y + 13*factor)     
        self.show_text(self.screen, "   \:::\   \::::/    /      \:::\    \        \:::\__/:::/    /       \:::\    \                   |::|   |             \:::\   \:::\____\\", 10, YELLOW, x, y + 14*factor)    
        self.show_text(self.screen, "    \:::\  /:::/    /        \:::\    \        \::::::::/    /         \:::\    \                  |::|   |              \:::\  /:::/    /", 10, YELLOW, x, y + 15*factor)    
        self.show_text(self.screen, "     \:::\/:::/    /          \:::\    \        \::::::/    /           \:::\    \                 |::|   |               \:::\/:::/    /", 10, YELLOW, x, y + 16*factor)     
        self.show_text(self.screen, "      \::::::/    /            \:::\    \        \::::/    /             \:::\    \                |::|   |                \::::::/    /", 10, YELLOW, x, y + 17*factor)      
        self.show_text(self.screen, "       \::::/    /              \:::\____\        \::/____/               \:::\____\               \::|   |                 \::::/    /", 10, YELLOW, x, y + 18*factor)       
        self.show_text(self.screen, "        \::/____/                \::/    /         ~~                      \::/    /                \:|   |                  \::/    /", 10, YELLOW, x, y + 19*factor)        
        self.show_text(self.screen, "         ~~                       \/____/                                   \/____/                  \|___|                   \/____/", 10, YELLOW, x, y + 20*factor)
        self.show_text(self.screen, "PRESS ANY KEY TO START", 20, GREEN, x+20, y + 23*factor)
        pg.display.flip()
    
    #third screen, for the win condition.
    def display_win_screen(self):
        self.screen.fill(STARTBG)
        x = WIDTH/2
        y = HEIGHT/4
        factor = 15
        self.show_text(self.screen, "          _____                    _____           _______                   _____                    _____                    _____", 10, YELLOW, x, y+factor )
        self.show_text(self.screen, "         /\    \                  /\    \         /::\    \                 /\    \                  /\    \                  /\    \\", 10, YELLOW, x, y + 2*factor)
        self.show_text(self.screen, "        /::\    \                /::\____\       /::::\    \               /::\    \                /::\____\                /::\    \\", 10, YELLOW, x, y + 3*factor)
        self.show_text(self.screen, "       /::::\    \              /:::/    /      /::::::\    \             /::::\    \              /:::/    /               /::::\    \\", 10, YELLOW, x, y + 4*factor)
        self.show_text(self.screen, "      /::::::\    \            /:::/    /      /::::::::\    \           /::::::\    \            /:::/    /               /::::::\    \\", 10, YELLOW, x, y + 5*factor)
        self.show_text(self.screen, "     /:::/\:::\    \          /:::/    /      /:::/~~\:::\    \         /:::/\:::\    \          /:::/    /               /:::/\:::\    \\", 10, YELLOW, x, y + 6*factor)
        self.show_text(self.screen, "    /:::/__\:::\    \        /:::/    /      /:::/    \:::\    \       /:::/  \:::\    \        /:::/____/               /:::/__\:::\    \\", 10, YELLOW, x, y + 7*factor)
        self.show_text(self.screen, "   /::::\   \:::\    \      /:::/    /      /:::/    / \:::\    \     /:::/    \:::\    \      /::::\    \               \:::\   \:::\    \\", 10, YELLOW, x, y + 8*factor)
        self.show_text(self.screen, "  /::::::\   \:::\    \    /:::/    /      /:::/____/   \:::\____\   /:::/    / \:::\    \    /::::::\____\________    ___\:::\   \:::\    \\", 10, YELLOW, x+5, y + 8*factor)
        self.show_text(self.screen, " /:::/\:::\   \:::\ ___\  /:::/    /      |:::|    |     |:::|    | /:::/    /   \:::\    \  /:::/\:::::::::::\    \  /\   \:::\   \:::\    \\", 10, YELLOW, x+5, y + 9*factor) 
        self.show_text(self.screen, "/:::/__\:::\   \:::|    |/:::/____/       |:::|____|     |:::|    |/:::/____/     \:::\____\/:::/  |:::::::::::\____\/::\   \:::\   \:::\____\\", 10, YELLOW, x+5, y + 10*factor)
        self.show_text(self.screen, "\:::\   \:::\  /:::|____|\:::\    \        \:::\    \   /:::/    / \:::\    \      \::/    /\::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /", 10, YELLOW, x, y + 11*factor)
        self.show_text(self.screen, " \:::\   \:::\/:::/    /  \:::\    \        \:::\    \ /:::/    /   \:::\    \      \/____/  \/____|::|   |           \:::\   \:::\   \/____/", 10, YELLOW, x, y + 12*factor)
        self.show_text(self.screen, "  \:::\   \::::::/    /    \:::\    \        \:::\    /:::/    /     \:::\    \                    |::|   |            \:::\   \:::\    \\", 10, YELLOW, x-10, y + 13*factor)     
        self.show_text(self.screen, "   \:::\   \::::/    /      \:::\    \        \:::\__/:::/    /       \:::\    \                   |::|   |             \:::\   \:::\____\\", 10, YELLOW, x, y + 14*factor)    
        self.show_text(self.screen, "    \:::\  /:::/    /        \:::\    \        \::::::::/    /         \:::\    \                  |::|   |              \:::\  /:::/    /", 10, YELLOW, x, y + 15*factor)    
        self.show_text(self.screen, "     \:::\/:::/    /          \:::\    \        \::::::/    /           \:::\    \                 |::|   |               \:::\/:::/    /", 10, YELLOW, x, y + 16*factor)     
        self.show_text(self.screen, "      \::::::/    /            \:::\    \        \::::/    /             \:::\    \                |::|   |                \::::::/    /", 10, YELLOW, x, y + 17*factor)      
        self.show_text(self.screen, "       \::::/    /              \:::\____\        \::/____/               \:::\____\               \::|   |                 \::::/    /", 10, YELLOW, x, y + 18*factor)       
        self.show_text(self.screen, "        \::/____/                \::/    /         ~~                      \::/    /                \:|   |                  \::/    /", 10, YELLOW, x, y + 19*factor)        
        self.show_text(self.screen, "         ~~                       \/____/                                   \/____/                  \|___|                   \/____/", 10, YELLOW, x, y + 20*factor)
        self.show_text(self.screen, "YOU WON, closing game...", 20, GREEN, x+20, y + 23*factor)
        pg.display.flip()

    def display_shop_screen(self):
        self.screen.fill(STARTBG)
        x = WIDTH/2
        y = HEIGHT/4
        factor = 15 # factor added for easy modification
        self.show_text(self.screen, "this is the shop", 20, YELLOW, x, y+factor )
        self.show_text(self.screen, "Press 1 for 1x interlaced destiny", 20, YELLOW, x, y+1*factor )
        self.show_text(self.screen, "Press 2 for invincibility", 20, YELLOW, x, y+2*factor )
        pg.display.flip()

#way to detect if any key on the keyboard is pressed
    #Coach Cozort's Code referenced
    def press_any_key(self):
        waiting = True
        while waiting:
            pg.event.clear()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    #we have defined the run method in the game engine
    def run(self):
        self.playing = True
        while self.playing: #and not self.game_paused:
            self.dt = self.clock.tick(FPS) / 1000
            self.timer -= 0.00550625
            self.events()
            self.update()
            self.draw()
            pg.display.flip()
            if self.player.lives == 0 or int(self.timer) == 0:
                g.display_end_screen()
                time.sleep(5)
                self.quit()
            if g.player.score == 36:
                g.display_win_screen()
                time.sleep(5)
                self.quit()
            # input process output
  
    # initializing all variables and setting up groups and instantiating classes
    def new(self):
        pg.time.set_timer(pg.USEREVENT, 599)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.invincibility = pg.sprite.Group()
        self.ptw = pg.sprite.Group()
        self.walltp = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            #print(row)
            print(tiles)
            for col, tile in enumerate(tiles):
                #print(col)
                print(tile)
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "E":
                    Enemy(self, col, row)
                if tile == "C":
                    Coin(self, col, row)
                if tile == "G":
                    Vertenemy(self, col, row)
                if tile == "T":
                    WallTP(self, col, row)

#    def topbar(self):
#        while self.playing:

    #Quits pygame window and closes it
    def quit(self):
        pg.quit()
        sys.exit()

    #updates all sprites
    def update(self):
        self.all_sprites.update()
        #self.cooldown.ticking()
        # single line updates all sprites, is repeatedly called

    #not actually used anymore, but this would draw a grid at the borders of every square in the game
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    #When called, it repeatedly draws everything in the game
    def draw(self):
        self.screen.fill(BGCOLOR)
#        self.draw_grid()
        self.all_sprites.draw(self.screen)
        #added the text here so it gets drawn over the other elements! (issue in previous push)
        self.show_text(self.screen, "Score: " + str(self.player.score), 25, RED, 75, 0)
        self.show_text(self.screen, "Time Left " + str(int(self.timer)), 25, RED, 300, 0)
        #self.show_text(self.screen, "EAT ALL THE COINS", 25, RED, 550, 0)
        self.show_text(self.screen, "HP " + str(self.player.lives), 25, RED, 560, 0)
        if self.player.tptimer == 0:
            self.show_text(self.screen, "TRAPPED ", 35, RED, 560, 380)
        self.show_text(self.screen, "Speed " + str(200 + (self.player.score*10)), 25, RED, 700, 0)
        self.show_text(self.screen, "Primegem " + str(self.player.primegem), 25, RED, 900, 0) 
        pg.display.flip()

    #this tracks pressing the x button on window
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def show_go_screen(self):
        pass

#I have instantiated the game
g = Game()

g.display_startup_screen()
# running to see if any key is pressed, then it runs g.new
g.press_any_key();
g.new()
g.run()
g.topbar()
g.press_any_key()
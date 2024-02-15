#1st space game 
import pygame
import os
import time
import random

pygame.font.init()

#WINDOW CODE

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Bubble project")




# ALL ASSETS LOAD 

#Loads images
RED_SPACESHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACESHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACESHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#Player player 
YELLOW_SPACESHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#Lasers
Red_Laser = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
Green_Laser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
Blue_Laser = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
Yellow_Laser = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")), (WIDTH,HEIGHT))
 

class Laser:
    def __init___(self, x, y, img  ):
        self.x =x 
        self.y = y 
        self.img = img 
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self,img, (self.x, self.y))

    def move(self,vel):
         self.y += vel
         
    def off_Screen(self,height):
        return self.y <= height and self.y >= 0
    
    def collision(self,obj):
        return collide(obj,self)


class Ship:      #UNDEFINED SHIP CLASS FOR INHARETANCE
    def __init__(self, x, y, health = 100):
        self.x = x 
        self.y = y
        self.health = health
        self.ship_img = None 
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0


    def draw(self, window): 
        window.blit(self.ship_img, (self.x, self.y))

    def get_widht(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACESHIP
        self.laser_img = Yellow_Laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
          "red": (RED_SPACESHIP, Red_Laser),
            "green": (GREEN_SPACESHIP, Green_Laser),
            "blue": (BLUE_SPACESHIP,Blue_Laser)
    }


    def __init__(self, x, y, color,  health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self,vel):
        self.y += vel
        
#GAME MAIN LOOP 
def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 0
    lives = 5 
    main_font  = pygame.font.SysFont("Times new roman", 50)
    lost_font  = pygame.font.SysFont("Times new roman", 70)
    
    enemies = []
    wave_length = 5
    enemy_vel = 1


    player_vel = 5 

    player =  Ship(300,65)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))             #OPERATES BACKGROUIDN IMG
        #draw text lives and points
        lives_label = main_font.render(f"Lives: {lives}",1 , (255,255,255,))
        level_label = main_font.render(f"Level: {level}",1 , (255,255,255))

        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10,10))


        for enemy in enemies:
            enemy.draw(WIN)


        player.draw(WIN)

        if lost: 
            lost_label = lost_font.render('You lost!!',1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2-lost_label.get_width()/2,350))

        pygame.display.update()




    while run: 
        clock.tick(FPS)                #DEFINES FPS FOR RUNNING GAME 
        redraw_window()


        if lives <= 0 or player.health <=0:
            lost = True
            lost_count += 1 

        if lost: 
            if lost_count > FPS * 3:
                run = False
            else:
                continue



        if len(enemies) == 0:
            level += 1
            wave_length += 5  
            for i in range(wave_length):
               enemy = Enemy(random.randrange(50, WIDTH -100), random.randrange(-1500,-100), random.choice(["red","blue","green"]))
               enemies.append(enemy)
               

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 run = False

        keys = pygame.key.get_pressed()                      # MOVMENT OF CHARACTER
        if keys[pygame.K_a] and player.x - player_vel > 0:               #Moves left if press "A" on keyboard
            player.x -= player_vel 
        if keys[pygame.K_d]and player.x + player_vel + player.get_widht() < WIDTH:               #Moves right if press "D" on keyboard
            player.x += player_vel           
        if keys[pygame.K_w]and player.y + player_vel > 0 :               #Moves up if press "W" on keyboard
            player.y -= player_vel   
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:             #Moves down if press "S" on keyboard
            player.y += player_vel 

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()

        
main()

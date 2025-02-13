import pygame
import sys
import random
import os

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Bird_image = pygame.image.load("game_images/bird3.png").convert_alpha()
class Bird:
    image = Bird_image
    max_rotaton = 25 
    rotation_velo = 20 
    Animation_time = 5

    def __init__(self,image, x, y ):
        self.x = x 
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img = self.image
        self.rect = self.image.get_rect(center=x)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def jump(self):
        self.vel = -10.5
        self.height = self.y

        
        
        

   


pipe = []
pipe_interval = 1500 #ms between adding new pipes 
pygame.time.set_timer(pygame.USEREVENT, pipe_interval)
pipe_image = pygame.image.load("game_images/pipe.png").convert_alpha()
score = 0
font = pygame.font.SysFont(None, 36)

background = pygame.image.load("game_images/background3.jpg").convert()
background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird = Bird('game_images/bird3.png', 30, 40)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    
    screen.blit(background, (0, 0))
    bird.draw(screen)
    
    pygame.display.flip()






    clock.tick(60)

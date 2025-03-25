#import packages to build the game
from __future__ import print_function
import pygame
import time
import os
import random

#initialize pygame
pygame.init()

#set up the screen to display the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 550
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#set up the font
FONT = pygame.font.SysFont('comicsansms', 20)
FONT_COLOR = (255, 255, 255) #white font

#load the required images
BIRD_IMGS = [pygame.image.load('game_images/bird1.png'),
             pygame.image.load('game_images/bird2.png'),
             pygame.image.load('game_images/bird3.png')]
BOTTOM_PIPE_IMG = pygame.image.load('game_images/pipe.png')
TOP_PIPE_IMG = pygame.transform.flip(BOTTOM_PIPE_IMG, False, True) #flip the image of the bottom pipe to get the image for the pipe on the top
FLOOR_IMG = pygame.image.load('game_images/base.png')
BG_IMG = pygame.transform.scale(pygame.image.load('game_images/bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
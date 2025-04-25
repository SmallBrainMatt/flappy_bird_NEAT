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

# Initialize the font properly
try:
    # We need to properly initialize the font module first
    if not pygame.font.get_init():
        pygame.font.init()
    
    # Try to use SysFont
    FONT = pygame.font.SysFont('comicsansms', 20)
except Exception as e:
    print(f"Error loading SysFont: {e}")
    try:
        # Fall back to default font
        FONT = pygame.font.Font(None, 20)
    except Exception as e:
        print(f"Error loading default font: {e}")
        # Last resort - create a minimal font renderer that won't crash
        class DummyFont:
            def render(self, text, antialias, color):
                # Return a small empty surface with the right dimensions
                text_size = (len(text) * 10, 20)
                surf = pygame.Surface(text_size)
                surf.fill((0, 0, 0))  # Black background
                return surf
        FONT = DummyFont()
        print("Using dummy font renderer as fallback")

FONT_COLOR = (255, 255, 255) #white font

#load the required images
BIRD_IMGS = [pygame.image.load('game_images/bird1.png'),
             pygame.image.load('game_images/bird2.png'),
             pygame.image.load('game_images/bird3.png')]
BOTTOM_PIPE_IMG = pygame.image.load('game_images/pipe.png')
TOP_PIPE_IMG = pygame.transform.flip(BOTTOM_PIPE_IMG, False, True) #flip the image of the bottom pipe to get the image for the pipe on the top
FLOOR_IMG = pygame.image.load('game_images/base.png')
BG_IMG = pygame.transform.scale(pygame.image.load('game_images/bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
import pygame
import sys
import random
import os
import time

pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode(SCREEN_WIDTH, SCREEN_HEIGHT)
pygmae.display.set_caption("FAPPY BIRD")

pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("game_images","pipe.png")).convert_alpha())
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("game_images","base.png")).convert_alpha())
background_image = pygame.transform.scale(pygame.image.load(os.path.join("game_images","bg.png")).convert_alpha(), (600,900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("game_images","bird" + str(x) +".png"))) for x in range(1,4)]



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

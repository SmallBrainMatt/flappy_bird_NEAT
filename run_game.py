import pygame
import neat
import os
import sys
import time
from main_game import main

def run(config_path):
    """
    Run the NEAT algorithm to train a neural network to play flappy bird
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
    
    # Create the population
    population = neat.Population(config)
    
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    # population.add_reporter(neat.Checkpointer(5))
    
    winner = population.run(main, 10)
    
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path) 

    #watch this shit pussy
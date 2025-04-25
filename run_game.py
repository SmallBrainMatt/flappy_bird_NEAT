import pygame
import neat
import os
import sys
import numpy as np
import pandas as pd
from main_game import main  # Import the correct main function

# Initialize generation data storage
generation_data = []

# Properly defined eval_genomes function
def eval_genomes(genomes, config):
    global generation_data
    
    # Run your main NEAT game loop to calculate fitness
    main(genomes, config)

    # Gather stats after main run completes
    scores = [genome.fitness for _, genome in genomes]
    complexities = [len(genome.connections) for _, genome in genomes]

    # Store metrics clearly after each generation
    generation_metrics = {
        'Generation': len(generation_data),
        'Best_Fitness': max(scores),
        'Average_Fitness': np.mean(scores),
        'Num_Species': None,  # We will handle this differently
        'Average_Score': np.mean(scores),
        'Max_Score': max(scores),
        'Average_Complexity': np.mean(complexities),
    }

    generation_data.append(generation_metrics)

# Main NEAT execution
def run_neat(config_path):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)

    # Add reporting for easier debugging and visualization
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run NEAT algorithm (adjust generation number if needed)
    winner = population.run(eval_genomes, 50)  # 50 generations for example

    # Save data to CSV
    results_df = pd.DataFrame(generation_data)
    results_df.to_csv('neat_results.csv', index=False)

    print("Training Complete! Data saved to neat_results.csv.")

# Run script directly
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')  # Ensure you have a config.txt file
    run_neat(config_path)
    

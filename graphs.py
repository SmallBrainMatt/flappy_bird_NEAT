"""
Simple 3-input example for NEAT.
"""

import os
import neat
import visualize
import glob

# 3-input sample inputs and expected outputs (example dataset).
sample_inputs = [
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0),
    (1.0, 0.0, 0.0),
    (1.0, 1.0, 1.0)
]
sample_outputs = [
    (0.0,),
    (1.0,),
    (1.0,),
    (1.0,),
    (0.0,)
]


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = len(sample_inputs)  # Start fitness at maximum possible
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(sample_inputs, sample_outputs):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0]) ** 2  # Mean Squared Error penalty


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population.
    p = neat.Population(config)

    # Add reporters.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations or until fitness_threshold is reached.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Test the winning network.
    print('\nTesting winner:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(sample_inputs, sample_outputs):
        output = winner_net.activate(xi)
        print(f"input: {xi}, expected: {xo}, got: {output}")

    # Visualizations
    node_names = {-1: 'Input1', -2: 'Input2', -3: 'Input3', 0: 'Output'}
    visualize.draw_net(config, winner, view=True)
    visualize.draw_net(config, winner, view=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    visualize.draw_net(config, winner, view=False, filename="best_network", node_names=node_names)


    # Restore from checkpoint and run a few more generations
    restored_p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    restored_p.run(eval_genomes, 10)
    for file in glob.glob("neat-checkpoint-*"):
        os.remove(file)
        print("Deleted all checkpoint files.")

if __name__ == '__main__':
    # Find config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)


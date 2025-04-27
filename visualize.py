import os
import graphviz
import matplotlib.pyplot as plt
import numpy as np

def draw_net(config, genome, view=False, filename=None, node_names=None,
             show_disabled=True, prune_unused=False, node_colors=None, fmt='png'):
    """Draws a neat neural network with graphviz."""
    from graphviz import Digraph

    if graphviz is None:
        raise ImportError("This function requires graphviz but it is not installed.")

    if node_names is None:
        node_names = {}

    if node_colors is None:
        node_colors = {}

    # Attributes for graphviz
    dot = Digraph(format=fmt, engine="dot")
    dot.attr(rankdir='LR')  # Left to Right

    inputs = set()
    outputs = set()

    for k in config.genome_config.input_keys:
        inputs.add(k)
    for k in config.genome_config.output_keys:
        outputs.add(k)

    used_nodes = set(inputs) | set(outputs)
    if prune_unused:
        connections = [cg.key for cg in genome.connections.values() if cg.enabled or show_disabled]
        for a, b in connections:
            used_nodes.add(a)
            used_nodes.add(b)

    # Draw input nodes
    for node in inputs:
        name = node_names.get(node, str(node))
        dot.node(name, _attributes={"shape": "box", "style": "filled", "fillcolor": node_colors.get(node, 'lightgray')})

    # Draw output nodes
    for node in outputs:
        name = node_names.get(node, str(node))
        dot.node(name, _attributes={"shape": "box", "style": "filled", "fillcolor": node_colors.get(node, 'lightblue')})

    # Draw hidden nodes
    for node in genome.nodes.keys():
        if node in inputs or node in outputs:
            continue
        if prune_unused and node not in used_nodes:
            continue
        name = node_names.get(node, str(node))
        dot.node(name, _attributes={"shape": "circle", "style": "filled", "fillcolor": node_colors.get(node, 'white')})

    # Draw connections
    for conn_key, conn in genome.connections.items():
        if prune_unused and (conn_key[0] not in used_nodes or conn_key[1] not in used_nodes):
            continue
        if not show_disabled and not conn.enabled:
            continue

        input_node, output_node = conn_key
        input_name = node_names.get(input_node, str(input_node))
        output_name = node_names.get(output_node, str(output_node))

        style = 'solid' if conn.enabled else 'dotted'
        color = 'green' if conn.weight > 0 else 'red'
        width = str(0.1 + abs(conn.weight / 5.0))  # Thicker lines for stronger weights

        dot.edge(input_name, output_name, _attributes={"style": style, "color": color, "penwidth": width})

    # Save or view
    if filename is None:
        filename = 'network'
    dot.render(filename, view=view)

def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.svg'):
    """Plots the population's average and best fitness."""
    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    plt.figure()
    plt.plot(generation, avg_fitness, 'b-', label="average")
    plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="best")
    plt.title("Population's average and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend()

    plt.savefig(filename)
    if view:
        plt.show()

def plot_species(statistics, view=False, filename='speciation.svg'):
    """Visualizes speciation throughout evolution."""
    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    plt.figure()
    plt.stackplot(range(num_generations), *curves)

    plt.title('Speciation')
    plt.xlabel('Generations')
    plt.ylabel('Size per Species')
    plt.grid()

    plt.savefig(filename)
    if view:
        plt.show()

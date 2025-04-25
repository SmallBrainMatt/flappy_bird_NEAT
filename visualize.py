import os
import graphviz

def draw_net(config, genome, view=False, filename="network_structure", show_disabled=True):
    dot = graphviz.Digraph(format='png', filename=filename)
    
    # Input nodes
    for i in range(config.genome_config.num_inputs):
        dot.node(f'input_{i}', f'Input {i}', shape='box')
    
    # Output nodes
    for i in range(config.genome_config.num_outputs):
        dot.node(f'output_{i}', f'Output {i}', shape='box')

    # Hidden nodes
    for node_id in genome.nodes:
        if node_id >= config.genome_config.num_inputs + config.genome_config.num_outputs:
            dot.node(str(node_id), f'Hidden {node_id}')

    # Connections
    for cg in genome.connections.values():
        if not cg.enabled and not show_disabled:
            continue
        dot.edge(str(cg.key[0]), str(cg.key[1]), style='solid' if cg.enabled else 'dotted')

    dot.render(view=view)

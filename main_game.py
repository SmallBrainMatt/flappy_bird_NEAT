from bird_builder import Bird
from pipe_builder import Pipe
from base_builder import Base
import game_initialization as gi
import game_parameter_setting as gp
import neat
import os
import pygame
from check_collision import collide
from draw_game import draw_game

# Function to get the index of the next pipe to use as input for neural network
def get_index(pipes, bird):
    if not pipes:
        return 0
    
    bird_x = bird.x
    
    # Find all pipes ahead of the bird
    ahead_pipes = [i for i, pipe in enumerate(pipes) if pipe.x + pipe.IMG_WIDTH > bird_x]
    
    if ahead_pipes:
        # Get the closest pipe ahead of the bird
        closest_pipe_idx = min(ahead_pipes, key=lambda i: pipes[i].x - bird_x)
        return closest_pipe_idx
    
    # If no pipes ahead (rare case), return the first pipe
    return 0

# Function to find all pipes that could potentially collide with the bird
def get_relevant_pipes(pipes, bird_x):
    relevant_pipes = []
    for pipe in pipes:
        # Is the pipe close enough to be relevant for collision?
        if pipe.x - 100 < bird_x < pipe.x + pipe.IMG_WIDTH + 100:
            relevant_pipes.append(pipe)
    return relevant_pipes

# Global variable to track generation
generation = 0

# Define the probability threshold to jump
prob_threshold_to_jump = 0.3
# Punishment for failing
failed_punishment = 50.0

#define a function to run the main game loop
def main(genomes, config):

    screen = gi.SCREEN
    font = gi.FONT
    bg = gi.BG_IMG
    
    global generation #use the global variable gen and SCREEN
    generation += 1 #update the generation
    
    clock = pygame.time.Clock() #set up a clock object to help control the game framerate
    start_time = pygame.time.get_ticks() #reset the start_time after every time we update our generation
    
    floor = Base(gp.floor_starting_y_position) #build the floor
    # Create pipes with proper spacing, ensuring we don't exceed the maximum number
    pipes_list = []
    for i in range(gp.pipe_max_num):
        x_pos = gp.pipe_starting_x_position + (i * gp.pipe_horizontal_gap)
        # Only create pipes that will be visible initially
        if x_pos < gi.SCREEN_WIDTH * 2:
            pipes_list.append(Pipe(x_pos))
    
    models_list = [] #create an empty list to store all the training neural networks
    genomes_list = [] #create an empty list to store all the training genomes
    birds_list = [] #create an empty list to store all the training birds
    
    # Instead of using indices as keys, we'll use bird objects as keys
    bird_scores = {}
    # Keep track of passed pipes using pipe indices and bird objects
    passed_pipe_ids = set()
    # Track the highest score achieved in this generation
    generation_max_score = 0
    
    for genome_id, genome in genomes: #for each genome
        bird = Bird(gp.bird_starting_x_position, gp.bird_starting_y_position)
        birds_list.append(bird) #create a bird and append the bird in the list
        genome.fitness = 0 #start with fitness of 0
        genomes_list.append(genome) #append the genome in the list
        model = neat.nn.FeedForwardNetwork.create(genome, config) #set up the neural network for each genome using the configuration we set
        models_list.append(model) #append the neural network in the list
        bird_scores[bird] = 0  # Initialize score for this bird using the bird object as key
        
    run = True
    max_score = 0  # Track the highest score for display
    
    while run is True: #when we run the program
        
        #check the event of the game and quit if we close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        
        #stop the game when the score exceed the maximum score
        #break the loop and restart when no bird left
        if max_score >= gp.max_score or len(birds_list) == 0:
            run = False
            break
        
        game_time = round((pygame.time.get_ticks() - start_time)/1000, 2) #record the game time for this generation
        
        clock.tick(gp.FPS) #update the clock, run at FPS frames per second (FPS). This can be used to help limit the runtime speed of a game.
        
        floor.move() #move the floor
        
        # Track pipes that are passed by birds
        for pipe_idx, pipe in enumerate(pipes_list):
            pipe.move() #move the pipe
            
            # Reset pipes that go off-screen
            if pipe.x + pipe.IMG_WIDTH < 0:
                # Find the rightmost pipe that's visible or just off-screen to the right
                visible_pipes = [p for p in pipes_list if p.x < gi.SCREEN_WIDTH * 2]
                if visible_pipes:
                    rightmost_pipe = max(visible_pipes, key=lambda p: p.x)
                    pipe.x = rightmost_pipe.x + gp.pipe_horizontal_gap
                    pipe.random_height() # generate random height for new pipe

                    old_pipe_ids = [pid for pid in passed_pipe_ids if pid.startswith(f"{pipe_idx}-")]
                    for old_id in old_pipe_ids:
                        passed_pipe_ids.remove(old_id)
                    if pipe.x > gp.pipe_starting_x_position + (gp.pipe_max_num - 1) * gp.pipe_horizontal_gap:
                        pipe.x = gp.pipe_starting_x_position
                else:
                    pipe.x = gp.pipe_starting_x_position
                    pipe.random_height()
                    
            
            # Check if any bird has passed this pipe
            for bird_idx, bird in enumerate(birds_list):
                # Create a unique identifier using the pipe's index and bird's memory address
                pipe_id = f"{pipe_idx}-{id(bird)}"
                
                # Only count the pipe as passed if it's ahead of the bird and hasn't been passed before
                if pipe.x + pipe.IMG_WIDTH < bird.x and pipe_id not in passed_pipe_ids:
                    passed_pipe_ids.add(pipe_id)  # Mark this pipe as passed for this bird
                    
                    # Safely increment the bird's score
                    if bird in bird_scores:
                        bird_scores[bird] += 1
                        print(f"Bird {bird_idx} passed pipe {pipe_idx}! Score: {bird_scores[bird]}")
                        
                        # Update max score if this bird has the highest score
                        if bird_scores[bird] > generation_max_score:
                            generation_max_score = bird_scores[bird]
                            max_score = generation_max_score
                            print(f"New max score: {max_score}")
        
        # Create a list to track birds that have failed
        birds_to_remove = []
        
        for index, bird in enumerate(birds_list):
            bird.move() #move the bird
            
            # Check if bird has hit the ceiling or floor first
            if bird.y <= 0 or bird.y + bird.bird_img.get_height() >= floor.y:
                birds_to_remove.append(index)
                continue
                
            # Check for collisions with pipes
            bird_failed = False
            relevant_pipes = get_relevant_pipes(pipes_list, bird.x)
            
            for pipe in relevant_pipes:
                if collide(bird, pipe, floor, screen):
                    bird_failed = True
                    break
                    
            # Calculate the specific pipe index for this bird
            bird_pipe_index = get_index(pipes_list, bird)
            
            # Make sure we have a valid pipe to use as input for neural network
            if bird_pipe_index < len(pipes_list):
                current_pipe = pipes_list[bird_pipe_index]
                
                # Input for neural network
                # Calculate the actual distance to the current pipe's center
                pipe_center_x = current_pipe.x + (current_pipe.IMG_WIDTH / 2)

                delta_x = pipe_center_x - bird.x  # Distance from bird to pipe center

                # Add breakpoint to inspect raw values
                # breakpoint()  # This will pause execution here
                
                # Normalize delta_x to be between -1 and 1 for better neural network input
                # Screen width is 800, so we'll normalize based on half that (400)
                delta_x = delta_x / 100  # This will give us a reasonable range
                
                delta_y_top = bird.y - current_pipe.top_pipe_height
                delta_y_bottom = current_pipe.bottom_pipe_topleft - bird.y
                
                # Add breakpoint to inspect normalized values
                # breakpoint()  # This will pause execution here
                
                # Normalize y distances based on screen height (550)
                # We'll use half the screen height (275) for normalization
                delta_y_top = delta_y_top / 175
                delta_y_bottom = delta_y_bottom / 175
                
                net_input = (delta_x, delta_y_top, delta_y_bottom)
                
                #input the bird's distance from the pipes to get the output of whether to jump or not
                output = models_list[index].activate(net_input)
                
                # Add breakpoint to inspect neural network output
                # breakpoint()  # This will pause execution here
                
                if output[0] > prob_threshold_to_jump: #if the model output is greater than the probability threshold to jump
                    # print("I jumped lol\n\n")
                    bird.jump() #then jump the bird
                
                # Get the current score for this bird
                bird_score = bird_scores.get(bird, 0)
                
                #the fitness function is a combination of game score, alive time, and a punishment for collision
                # Give more weight to passing pipes (multiply by 10) and less to survival time
                genomes_list[index].fitness = (bird_score * 5) + (game_time * 0.2) - bird_failed * failed_punishment
                
                if bird_failed:
                    birds_to_remove.append(index)
        
        # Remove failed birds, genomes, and models in reverse order to avoid index issues
        for index in sorted(birds_to_remove, reverse=True):
            if index < len(birds_list):
                bird = birds_list[index]
                # print(f"Bird {index} failed with score: {bird_scores.get(bird, 0)}")
                
                # Remove from all data structures
                if bird in bird_scores:
                    del bird_scores[bird]  # Remove the score for this bird
                    
                birds_list.pop(index)
                if index < len(genomes_list):
                    genomes_list.pop(index)
                if index < len(models_list):
                    models_list.pop(index)
                    
        # Print a summary of all bird scores every few seconds
        # if int(game_time) % 13 == 0 and game_time > 0:
            # print(f"\nTime: {game_time}s - Bird scores summary:")
            # Convert bird scores to indices for display
            # bird_indices = {birds_list.index(bird): score for bird, score in bird_scores.items() if bird in birds_list}
            # for idx, score in bird_indices.items():
                # print(f"Bird {idx}: {score}")
            # print(f"Max score: {max_score}, Birds alive: {len(birds_list)}\n")

        # Prepare score dictionary with indices for drawing
        display_scores = {birds_list.index(bird): score for bird, score in bird_scores.items() if bird in birds_list}
        
        # Draw the game, passing bird_scores to display on screen
        draw_game(screen, birds_list, pipes_list, floor, max_score, generation, game_time, display_scores) #draw the screen of the game

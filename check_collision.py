import pygame
import base_builder
import bird_builder
import pipe_builder
import game_parameter_setting
import game_initialization

#helper function to check collision
def collide(bird, pipe, base, screen):

    # This idea is to mask every object from the given surface by setting all the opaque pixels and not setting the transparent pixels
    bird_mask = pygame.mask.from_surface(bird.bird_img)
    top_pipe_mask = pygame.mask.from_surface(pipe.top_pipe_img)
    bottom_pipe_mask = pygame.mask.from_surface(pipe.bottom_pipe_img)

    sky_height = 0
    floor_height = base.y
    bird_lower_end = bird.y + bird.bird_img.get_height()

    # Calculate proper offsets for collision detection
    # Top pipe: Need to calculate the position of the bird relative to the pipe
    top_offset_x = pipe.x - bird.x
    top_offset_y = pipe.top_pipe_topleft - bird.y
    top_pipe_offset = (int(top_offset_x), int(top_offset_y))
    
    # Bottom pipe: Same concept
    bottom_offset_x = pipe.x - bird.x
    bottom_offset_y = pipe.bottom_pipe_topleft - bird.y
    bottom_pipe_offset = (int(bottom_offset_x), int(bottom_offset_y))

    # Check for collisions
    top_collision = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
    bottom_collision = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)

    # Check boundary collisions too
    boundary_collision = bird.y <= sky_height or bird_lower_end >= floor_height
    
    # Return True if any collision is detected
    if top_collision or bottom_collision or boundary_collision:
        return True
    else:
        return False
    
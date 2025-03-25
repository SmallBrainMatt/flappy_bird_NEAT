import pygame
import base_builder
import bird_builder
import pipe_builder
import game_initialization as gi
import game_parameter_setting as gp

def draw_game(screen, birds, pipes, base, max_score, generation, game_time, bird_scores=None):
    if bird_scores is None:
        bird_scores = {}
        
    #draw the background
    screen.blit(gi.BG_IMG, (0,0))

    #draw the moving floor
    screen.blit(base.IMGS[0], (base.x1, base.y))
    screen.blit(base.IMGS[1], (base.x2, base.y))
    screen.blit(base.IMGS[2], (base.x3, base.y))

    # Only draw pipes that are on screen
    for pipe in pipes:
        if -pipe.IMG_WIDTH < pipe.x < gi.SCREEN_WIDTH:
            screen.blit(pipe.top_pipe_img, (pipe.x, pipe.top_pipe_topleft)) #draw the pipe on the top
            screen.blit(pipe.bottom_pipe_img, (pipe.x, pipe.bottom_pipe_topleft))

    # Draw birds with their scores above them
    for i, bird in enumerate(birds):
        rotated_image, rotated_rect = bird.update()
        screen.blit(rotated_image, rotated_rect)
        
        # Show the bird's score above it
        if i in bird_scores:
            score_label = gi.FONT.render(f"{bird_scores[i]}", 1, (255, 0, 0))  # Red text for scores
            screen.blit(score_label, (bird.x - 10, bird.y - 25))  # Position above bird

    # Draw UI elements
    score_text = gi.FONT.render('Max Score: ' + str(max_score), 1, gi.FONT_COLOR)
    screen.blit(score_text, (gi.SCREEN_WIDTH - 15 - score_text.get_width(), 15))

    game_time_text = gi.FONT.render('Timer: ' + str(game_time) + 's', 1, gi.FONT_COLOR)
    screen.blit(game_time_text, (gi.SCREEN_WIDTH - 15 - game_time_text.get_width(), 15 + score_text.get_height()))

    generation_text = gi.FONT.render('Generation: ' + str(generation - 1), 1, gi.FONT_COLOR)
    screen.blit(generation_text, (15, 15))

    bird_text = gi.FONT.render('Birds Alive: ' + str(len(birds)), 1, gi.FONT_COLOR)
    screen.blit(bird_text, (15, 15 + generation_text.get_height()))

    progress_text = gi.FONT.render('Pipes Remaining: ' + str(len(pipes)), 1, gi.FONT_COLOR)
    screen.blit(progress_text, (15, 15 + generation_text.get_height() + bird_text.get_height()))

    pygame.display.update()
    
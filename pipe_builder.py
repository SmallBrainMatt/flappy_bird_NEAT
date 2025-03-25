import game_parameter_setting as gp
import game_initialization as gi
import random

class Pipe:
    VERTIVAL_GAP = gp.pipe_vertical_gap
    VELOCITY = gp.pipe_velocity
    IMG_WIDTH = gi.TOP_PIPE_IMG.get_width()
    IMG_LENGTH = gi.TOP_PIPE_IMG.get_height()

    def __init__(self, x_pos):
        self.top_pipe_img = gi.TOP_PIPE_IMG
        self.bottom_pipe_img = gi.BOTTOM_PIPE_IMG
        self.x = x_pos
        self.top_pipe_height = 0
        self.top_pipe_topleft = 0
        self.bottom_pipe_topleft = 0
        self.random_height()

    def move(self):
        self.x -= self.VELOCITY
        
    def random_height(self):
        # Get a random height for the top pipe
        self.top_pipe_height = random.randrange(gp.top_pipe_min_height, gp.top_pipe_max_height)
        
        # Calculate the top-left corner of the top pipe
        # This will be negative (above the top of the screen)
        self.top_pipe_topleft = self.top_pipe_height - self.IMG_LENGTH
        
        # Calculate the top-left corner of the bottom pipe
        # This should be positioned below the top pipe with the vertical gap in between
        self.bottom_pipe_topleft = self.top_pipe_height + self.VERTIVAL_GAP

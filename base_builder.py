import game_initialization as gi
import game_parameter_setting as gp

class Base:

    IMGS = [gi.FLOOR_IMG, gi.FLOOR_IMG, gi.FLOOR_IMG] 
    VELOCITY = gp.floor_velocity
    IMG_WIDTH = gi.FLOOR_IMG.get_width()

    def __init__(self, y_pos):
        self.x1 = 0 
        self.x2 = self.IMG_WIDTH
        self.x3 = self.IMG_WIDTH * 2
        self.y = y_pos

    def move(self):
        # Move the floor segments to the left
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY
        self.x3 -= self.VELOCITY

        # Check if any floor segment has moved completely off the screen
        # If so, move it back to the right side to create a seamless scrolling effect
        if self.x1 + self.IMG_WIDTH < 0:
            self.x1 = max(self.x2, self.x3) + self.IMG_WIDTH
        
        if self.x2 + self.IMG_WIDTH < 0:
            self.x2 = max(self.x1, self.x3) + self.IMG_WIDTH
            
        if self.x3 + self.IMG_WIDTH < 0:
            self.x3 = max(self.x1, self.x2) + self.IMG_WIDTH
    
    
import pygame
import game_initialization as gi
import game_parameter_setting as gp
#lets build the bird class

class Bird:
    IMGS = gi.BIRD_IMGS
    MAX_UPWARD_ANGLE = gp.bird_max_upward_angle
    MAX_DOWNWARD_ANGLE = gp.bird_max_downward_angle

    #initialization of Bird Object
    def __init__(self, x_pos, y_pos):
        self.bird_img = self.IMGS[0]
        self.x = x_pos
        self.y = y_pos
        self.fly_angle = 0
        self.time = 0
        self.velocity = 0 
        self.index = 0 #used to change the bird images, set to 0. 


    def move(self):
        self.time += 1

        # displacement d of the bird after time t is based off of this formula d = vt + 1/2at^2
        displacement = self.velocity * self.time + (1/2) * gp.bird_acceleration * self.time**2

        if displacement > gp.bird_max_displacement:
            displacement = gp.bird_max_displacement

        self.y = self.y + displacement #update the bird y position after the displacement

        # if the bird is goig upward
        if displacement < 0:
            if self.fly_angle < self.MAX_UPWARD_ANGLE:
                self.fly_angle += max(gp.bird_angular_acceleration*(self.MAX_UPWARD_ANGLE - self.fly_angle), gp.bird_min_incremental_angle)
            
            elif self.fly_angle >= self.MAX_UPWARD_ANGLE:
                self.fly_angle = self.MAX_UPWARD_ANGLE
        else:
            if self.fly_angle > self.MAX_DOWNWARD_ANGLE:
                self.fly_angle -= abs(min(gp.bird_angular_acceleration*(self.MAX_UPWARD_ANGLE - self.fly_angle), -gp.bird_min_incremental_angle))
            elif self.fly_angle <= self.MAX_DOWNWARD_ANGLE:
                self.fly_angle = self.MAX_DOWNWARD_ANGLE

    def jump(self):
        self.velocity = gp.bird_jump_velocity 
        self.time = 0

    def update(self):
        #if the bird is diving, then it shouldn't flap its wings
        if self.fly_angle < -45:
            self.bird_img = self.IMGS[0]
            self.index = 0
        
        
        elif self.index >= len(self.IMGS):
            self.index = 0

        self.bird_img = self.IMGS[self.index]
        self.index += 1

        rotated_image = pygame.transform.rotate(self.bird_img, self.fly_angle)

        origin_img_center = self.bird_img.get_rect(topleft = (self.x, self.y)).center

        rotated_rect = rotated_image.get_rect(center = origin_img_center)

        return rotated_image, rotated_rect
        





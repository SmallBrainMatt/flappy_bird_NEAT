import pygame
import sys
import random
import os
import time

pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FAPPY BIRD")

pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("game_images","pipe.png")).convert_alpha())
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("game_images","base.png")).convert_alpha())
background_image = pygame.transform.scale(pygame.image.load(os.path.join("game_images","bg.png")).convert_alpha(), (600,900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("game_images","bird" + str(x) +".png"))) for x in range(1,4)]




class Bird:
    """Bird class.

    This class contains the bird object and its methods.

    :attr x: The x coordinate of the bird.
    :attr y: The y coordinate of the bird.
    :attr tilt: The tilt of the bird.
    :attr tick_count: The tick count of the bird.
    :attr vel: The velocity of the bird.
    :attr height: The height of the bird.
    :attr img_count: The image count of the bird.
    :attr img: The image of the bird.
    :attr IMGS: The list of images of the bird.
    :attr MAX_ROTATION: The maximum rotation of the bird.
    :attr ROT_VEL: The rotation velocity of the bird.
    :attr ANIMATION_TIME: The animation time of the bird.
    """
    IMGS = bird_images
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self) -> None:
        """This method makes the bird jump.
        
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self) -> None:
        """This method makes the bird move.

        :return: None
        """
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        self.y = self.y + d
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win) -> None:
        """This method draws the bird.
        
        :param win: The window of the game.
        :return: None"""
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 5:
            self.img = self.IMGS[1]
        elif self.img_count >= self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(pipe_image, False, True)
        self.PIPE_BOTTOM = pipe_image
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL
    
    def draw(self, win) -> None:
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
                
    def collide(self, bird) -> bool:
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bot_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bottom - round(bird.y))
        b_point = bird_mask.overlap(bot_mask, bot_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        return False
        
        
class Base:
    VEL = 5
    WIDTH = base_image.get_width()
    
    def __init__(self, y):
        self.y = y
        self.BASE_IMAGE = base_image
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self) -> None:
        self.x1 -=self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self):
        WIN.blit(self.BASE_IMAGE, (self.x1,self.y))
        WIN.blit(self.BASE_IMAGE, (self.x2,self.y))
        
    

def draw_window(win, birds, pipes, base, score) -> None:
    win.blit(background_image, (0,0))
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    win.blit(text, (10,10))
    pygame.display.update()
    
    
def main() -> None:
    
    nets = []
    ge = []
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    birds = []
    pipes = [Pipe(700)]
    base = [Base(730)]
    run =   True
    score = 0
    clock = pygame.time.Clock()
    
    while run: 
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            pipe_num = 0
            if len(birds) > 0 :
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_num = 1
            else:
                run = False
                break
            for x, bird in enumerate(birds):
                bird.move()
            rem = []
            for pipe in pipes:
                for x, bird in enumerate(birds):
                    if pipe.collide(bird):
                        birds.pop(x)
                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)
                pipe.move()
            if add_pipe:
                score += 1
                pipes.append(Pipe(700))
            for r in rem:
                pipes.remove(r)
            for x, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                    birds.pop(x)
            base.move()
            draw_window(win, birds, pipes, base, score)
                
        
if __name__ == '__main__':
    main()

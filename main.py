import pygame
import neat
import time
import os

from ground import Ground
from bird import Bird
from pipe import Pipe

MIN_WIDTH = 500
MIN_HEIGHT = 800


BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))



def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)
    pygame.display.update()


ALLOWED_MARGIN = 10

def check_collision(bird, pipes, base):
    if bird.y <= 0 - ALLOWED_MARGIN:
        return True 
    if bird.y + bird.img.get_height() >= base.top:
        return True
    for pipe in pipes:
        l = pipe.x - bird.img.get_width() + ALLOWED_MARGIN
        r = pipe.x + pipe.img_top.get_width() - ALLOWED_MARGIN
        if bird.x >= l and bird.x <= r:
            if bird.y + ALLOWED_MARGIN <= pipe.top + pipe.img_top.get_height():
                return True
            if bird.y + bird.img.get_height() - ALLOWED_MARGIN >= pipe.bottom:
                return True
    return False


def main():
    bird = Bird(200, 200)
    ground = Ground(MIN_HEIGHT - 100)
    win = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    pipes = [Pipe(MIN_WIDTH)]
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                bird.jump()
        bird.move()
        
        for pipe in pipes:
            pipe.move()
      
        if(pipes[0].passed):
            pipes.pop(0)
      
        if(pipes[-1].x <MIN_WIDTH/3):
            pipes.append(Pipe(MIN_WIDTH))
        
      
        if(check_collision(bird,pipes, ground)):
            run = False
        # else:
        draw_window(win, bird, pipes, ground)
    
    pygame.quit()
    quit()
    
main()
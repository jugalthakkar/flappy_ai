import pygame
import neat
import time
import os

from ground import Ground
from bird import Bird
from pipe import Pipe

WIN_WIDTH = 500
WIN_HEIGHT = 800
pygame.init()
pygame.mixer.init()
pygame.font.init()

JUMP_SOUND = pygame.mixer.Sound(os.path.join("sound","jump.mp3"))
JUMP_SOUND.set_volume(0.2)
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("sound","game-over.mp3"))
GAME_OVER_SOUND.set_volume(1)


BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

FONT = pygame.font.SysFont("comicsans",30,bold=True)

def draw_window(win, bird, pipes, ground, score):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    ground.draw(win)
    bird.draw(win)
    
    score_txt = FONT.render("Score: "+ str(score),True,(255,255,255))
    win.blit(score_txt,(10,10))
    
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
    ground = Ground(WIN_HEIGHT - 70)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flap Flap Flappy!!")
    clock = pygame.time.Clock()
    
    
    run = True
    pipes = [Pipe(WIN_WIDTH)]
    score = 0
    paused = False
    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif paused == False:
                    bird.jump()
                    JUMP_SOUND.play()
        if paused:
            continue  
        
        bird.move()
        ground.move()
        
        for pipe in pipes:
            pipe.move()
      
        if(pipes[0].passed == False and pipes[0].x +pipes[0].img_top.get_width() < bird.x):
            score += 1
            pipes[0].passed = True
            pipes.append(Pipe(WIN_WIDTH))
            
        if(pipes[0].x < -pipes[0].img_top.get_width()):
            pipes.pop(0)
      
        # if(pipes[-1].x <WIN_WIDTH/3):
            # pipes.append(Pipe(WIN_WIDTH))
        
      
        if(check_collision(bird,pipes, ground)):
            run = False
        # else:
        draw_window(win, bird, pipes, ground, score)
    
    GAME_OVER_SOUND.play()
    while True:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    
main()
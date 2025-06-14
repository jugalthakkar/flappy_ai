import neat.config
import pygame
import neat
import time
import os

from ground import Ground
from bird import Bird
from pipe import Pipe

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800


BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 30)


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
        
    text = STAT_FONT.render("Gen: " + str(gen),1,(255,255,255))
    win.blit(text,(10,10))
    
    text = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))
        
    pygame.display.update()


ALLOWED_MARGIN = 10
curr_gen = 0
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


def main(genomes, config):
    global curr_gen
    birds = []
    nets = []
    ge = []
    curr_gen += 1
    score = 0
    # WIN_SCORE_THRESHOLD will only apply during training (when multiple birds exist)
    WIN_SCORE_THRESHOLD = 50
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(200, 200))
        g.fitness = 0
        ge.append(g)
    
    ground = Ground(WIN_HEIGHT - 100)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    pipes = [Pipe(WIN_WIDTH)]
    while run:
        clock.tick(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
       
             
        deaths = []        
        for pipe in pipes:
            pipe.move()
      
        if(pipes[0].passed):
            pipes.pop(0)
      
        if(pipes[-1].x <WIN_WIDTH/(2 if score > 40 else (2.5 if score > 20 else 3))):
            pipes.append(Pipe(WIN_WIDTH))
            score += 1
            for i,g in enumerate(ge):
                if i not in deaths:
                    g.fitness += 5
            # Only apply early termination if there are multiple birds (i.e., during training)
            if len(birds) > 1 and score >= WIN_SCORE_THRESHOLD:
                run = False
                print(f"Generation {curr_gen} ended early due to a bird reaching score {score}")
                break
        
        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].img_top.get_width():
                pipe_idx = 1
        else:
            run = False
            break
        
        for i, bird in enumerate(birds):
            bird.move()
            if(check_collision(bird,pipes, ground)):
                deaths.append(i)
            else:
                ge[i].fitness += 0.1
                output = nets[i].activate((bird.y,abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))
                
                if output[0] > 0:
                    bird.jump()
                    

        # else:
        draw_window(win, birds, pipes, ground, score, curr_gen)
        deaths.sort(reverse=True)
        for i in deaths:
            ge[i].fitness -= 1
            birds.pop(i)
            nets.pop(i)
            ge.pop(i)
    
  

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    
    winner =p.run(main,100)
    # Added lines to run the game with the winner genome
    print('\nWINNER WINNER, CHICKEN DINNER!\n\nBest genome:\n{!s}'.format(winner))
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    main([(0, winner)], config)
    while True:
        pygame.time.Clock().tick(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config_feed_forward.txt")
    run(config_path)
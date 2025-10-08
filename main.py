import neat.config
import pygame
import neat
import time
import os
import pickle
import argparse

from ground import Ground
from bird import Bird
from pipe import Pipe

pygame.font.init()

SPEED = 20
WIN_SCORE_THRESHOLD = 50
MIN_SURVIVORS = 5
JUMP_THRESHOLD = 0

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

SCORE_FONT = pygame.font.SysFont("comicsans", 30)

STAT_FONT = pygame.font.SysFont("comicsans", 20)
WIN_WIDTH = 500
WIN_HEIGHT = 800


def draw_window(win, birds, pipes, base, score, gen, current_ge_list, initial_genomes_for_avg_calc):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
        
    text = STAT_FONT.render("Gen: " + str(gen),1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),50))
    
    text = STAT_FONT.render("Birds: " + str(len(birds)),1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),30))
    
    # Calculate and display average fitness
    avg_fitness = 0
    if len(initial_genomes_for_avg_calc) > 0:
        total_fitness = sum(g.fitness for _, g in initial_genomes_for_avg_calc)
        avg_fitness = int(round(total_fitness / len(initial_genomes_for_avg_calc), 0))
    text = STAT_FONT.render("Avg Fitness: " + str(avg_fitness),1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),70))
    
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
    ge = []  # Initialize ge here
    initial_genomes_for_avg_calc = list(genomes)  # Store a copy of initial genomes for average fitness
    curr_gen += 1
    score = 0
    # WIN_SCORE_THRESHOLD will only apply during training (when multiple birds exist)

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
        
        clock.tick(SPEED)
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
      
        if(pipes[-1].x <WIN_WIDTH/(2.2 if score > 40 else (2.6 if score > 20 else 3))):
            pipes.append(Pipe(WIN_WIDTH))
            score += 1
            for i,g in enumerate(ge):
                if i not in deaths:
                    g.fitness += 5
            # Only apply early termination if there are multiple birds (i.e., during training)
            if len(genomes) > 1 and score >= WIN_SCORE_THRESHOLD:
                run = False
                print(f"Generation {curr_gen} ended early due to a bird reaching score {score}")
                break
        
        pipe_idx = 0
        if len(birds) > MIN_SURVIVORS:
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
                dLeft1 = pipes[pipe_idx].x - bird.x
                dRight1 = pipes[pipe_idx].x - bird.x + pipes[pipe_idx ].img_top.get_width()
                dTop1 = abs(bird.y - pipes[pipe_idx].height)
                dBottom1 = abs(bird.y - pipes[pipe_idx].bottom)
                if len(pipes) > pipe_idx + 1:
                    dTop2 = abs(bird.y - pipes[pipe_idx + 1].height)
                    dBottom2 = abs(bird.y - pipes[pipe_idx + 1].bottom)
                    dLeft2 = pipes[pipe_idx + 1].x - bird.x
                    dRight2 = pipes[pipe_idx].x - bird.x + pipes[pipe_idx + 1].img_top.get_width()
                else:
                    dTop2 = WIN_HEIGHT
                    dBottom2 = WIN_HEIGHT
                    dLeft2 = WIN_WIDTH
                    dRight2 = WIN_WIDTH
                output = nets[i].activate((bird.y,dLeft1,dRight1,dTop1, dBottom1,dLeft2,dRight2,dTop2, dBottom2))
                

                if output[0] > JUMP_THRESHOLD:
                    bird.jump()
                    

        # else:
        draw_window(win, birds, pipes, ground, score, curr_gen, ge, initial_genomes_for_avg_calc)
        deaths.sort(reverse=True)
        for i in deaths:
            ge[i].fitness -= 10
            birds.pop(i)
            nets.pop(i)
            ge.pop(i)
    
  

def run_game_with_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    bird = Bird(200, 200)
    ground = Ground(WIN_HEIGHT - 100)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    pipes = [Pipe(WIN_WIDTH)]
    score = 0
    run = True

    while run:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        bird.move()

        pipe_idx = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].img_top.get_width():
            pipe_idx = 1

        dLeft1 = pipes[pipe_idx].x - bird.x
        dRight1 = pipes[pipe_idx].x - bird.x + pipes[pipe_idx].img_top.get_width()
        dTop1 = abs(bird.y - pipes[pipe_idx].height)
        dBottom1 = abs(bird.y - pipes[pipe_idx].bottom)
        if len(pipes) > pipe_idx + 1:
            dTop2 = abs(bird.y - pipes[pipe_idx + 1].height)
            dBottom2 = abs(bird.y - pipes[pipe_idx + 1].bottom)
            dLeft2 = pipes[pipe_idx + 1].x - bird.x
            dRight2 = pipes[pipe_idx].x - bird.x + pipes[pipe_idx + 1].img_top.get_width()
        else:
            dTop2 = WIN_HEIGHT
            dBottom2 = WIN_HEIGHT
            dLeft2 = WIN_WIDTH
            dRight2 = WIN_WIDTH
        
        output = net.activate((bird.y, dLeft1, dRight1, dTop1, dBottom1, dLeft2, dRight2, dTop2, dBottom2))

        if output[0] > JUMP_THRESHOLD:
            bird.jump()
        
        rem_pipes = []
        for pipe in pipes:
            if pipe.x + pipe.img_top.get_width() < 0:
                rem_pipes.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
            pipe.move()
        
        for r_pipe in rem_pipes:
            pipes.remove(r_pipe)
        
        if pipes[-1].x < WIN_WIDTH - 200:
            pipes.append(Pipe(WIN_WIDTH))

        if check_collision(bird, pipes, ground):
            print(f"Game Over! Score: {score}")
            break # Exit the game loop on collision

        draw_window(win, [bird], pipes, ground, score, 0, [], [(0, genome)]) # Gen 0, empty ge, use single genome for avg fitness

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    
    winner =p.run(main,100)
    # Added lines to run the game with the winner genome
    print('\nWINNER WINNER, CHICKEN DINNER!\n\nBest genome:\n{!s}'.format(winner))
    
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    run_game_with_genome(winner, config) # Call the new function to run the winner
    # The previous while True loop is now handled within run_game_with_genome

def parse_arguments():
    parser = argparse.ArgumentParser(description="Flappy Bird AI with NEAT")
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'test'],
                        help='Mode to run the AI: train a new model or test an existing one.')
    parser.add_argument('--genome-path', type=str, default='best_genome.pkl',
                        help='Path to the .pkl file containing the trained genome (only for test mode).')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config_feed_forward.txt")

    if args.mode == 'train':
        run(config_path)
    elif args.mode == 'test':
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        try:
            with open(args.genome_path, "rb") as f:
                winner_genome = pickle.load(f)
        except FileNotFoundError:
            print(f"Error: Genome file not found at {args.genome_path}")
            quit()
        
        run_game_with_genome(winner_genome, config) # Call the new function for test mode
        # The previous while True loop is now handled within run_game_with_genome
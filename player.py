import os
import pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

from game import Game

WIN_WIDTH = 500
WIN_HEIGHT = 800
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("sound","game-over.mp3"))
GAME_OVER_SOUND.set_volume(1)


class Player:
    
    def __init__(self):
        pygame.display.set_caption("Flap Flap Flappy!!")
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        
    
    def _run_game(self):
        game = Game(self.win)
        run = True
        paused = False
        while run:
            self.clock.tick(30)
            event_for_game = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    else:
                        event_for_game = event

            if paused == False:
                game.play(event_for_game)
                run = not game.over
            pygame.display.update()
        return game.over
    
    def start(self):
        is_over = self._run_game()
        if is_over:
            GAME_OVER_SOUND.play()
        while True:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return self.start()

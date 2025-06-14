from bird import Bird
from ground import Ground
from pipe import Pipe
import pygame
import os

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

FONT = pygame.font.SysFont("comicsans",30,bold=True)

class Game:
    ALLOWED_MARGIN = 10
    def __init__(self, win):
        self.bird = Bird(200, 200)
        self.ground = Ground(win.get_height() - 70)
        self.pipes = [Pipe(win.get_width())]
        self.score = 0
        self.win = win
        self.over = False
        self.start = False

    def _handle_event(self, event):
        if event and event.key:
            if self.start:
                self.bird.jump()
            else:
                self.start = True

    def _check_collision(self):
        if self.bird.y <= 0 - self.ALLOWED_MARGIN:
            return True
        if self.bird.y + self.bird.img.get_height() >= self.ground.top:
            return True
        for pipe in self.pipes:
            l = pipe.x - self.bird.img.get_width() + self.ALLOWED_MARGIN
            r = pipe.x + pipe.img_top.get_width() - self.ALLOWED_MARGIN
            if self.bird.x >= l and self.bird.x <= r:
                if self.bird.y + self.ALLOWED_MARGIN <= pipe.top + pipe.img_top.get_height():
                    return True
                if self.bird.y + self.bird.img.get_height() - self.ALLOWED_MARGIN >= pipe.bottom:
                    return True
        return False

    def _update(self):
        if not self.start:
            return
        self.bird.move()
        self.ground.move()

        for pipe in self.pipes:
            pipe.move()

        if(self.pipes[0].passed == False and self.pipes[0].x +self.pipes[0].img_top.get_width() < self.bird.x):
            self.score += 1
            self.pipes[0].passed = True
            self.pipes.append(Pipe(self.win.get_width()))

        if(self.pipes[0].x < -self.pipes[0].img_top.get_width()):
            self.pipes.pop(0)


        if(self._check_collision()):
            self.over = True



    def _draw(self):
        self.win.blit(BG_IMG, (0,0))
        for pipe in self.pipes:
            pipe.draw(self.win)
        self.ground.draw(self.win)
        self.bird.draw(self.win)

        score_txt = FONT.render("Score: "+ str(self.score),True,(255,255,255))
        self.win.blit(score_txt,(10,10))


    def play(self, event):
        self._handle_event(event)
        self._update()
        self._draw()
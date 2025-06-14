import pygame
import random
import os

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os .path.join("imgs","pipe.png")))

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.img_top = pygame.transform.flip(PIPE_IMG, False, True)
        self.img_bottom = PIPE_IMG
        self.set_height()
        self.passed = False

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.img_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.img_top,(self.x,self.top))
        win.blit(self.img_bottom,(self.x,self.bottom))

import pygame
import os

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))


class Ground:

    def __init__(self, top):
        self.top = top
        self.img = BASE_IMG

    def draw(self, win):
        win.blit(self.img,(0,self.top))
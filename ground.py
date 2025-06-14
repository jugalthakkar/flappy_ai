import pygame
import os

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))


class Ground:
    VEL = 5

    def __init__(self, top):
        self.top = top
        self.img = BASE_IMG
        self.x1 = 0
        self.x2 = BASE_IMG.get_width()

    def draw(self, win):
        win.blit(self.img,(self.x1,self.top))
        win.blit(self.img,(self.x2,self.top))
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if(self.x1 < -self.img.get_width()):
            self.x1 += self.img.get_width() * 2
        if(self.x2 < -self.img.get_width()):
            self.x2 += self.img.get_width() * 2
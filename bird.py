import pygame
import os

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
JUMP_SOUND = pygame.mixer.Sound(os.path.join("sound","jump.mp3"))
JUMP_SOUND.set_volume(0.2)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 8
    ANIMATION_TIME = 5
    GRAVITY = 2.5
    

    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.tilt = 0
        self.velocity = velocity
        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.tick_count = 0

    def jump(self):
        # self.velocity = -15 if self.difficulty
        self.height = self.y
        self.tick_count = 0
        JUMP_SOUND.play()

    def move(self):
        self.tick_count += 1
        d = self.velocity * self.tick_count + 0.5 * self.GRAVITY * (self.tick_count ** 2)

        if self.height + d - self.y > 30:
            self.y += 30
        else:
            self.y = self.height + d
        # if d < 0:
        #     d -= 2

        

        if d < 0:
            self.tilt = self.MAX_ROTATION
        elif d > 0:
            self.tilt = max(self.tilt-self.ROT_VEL,-90)


    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_img, new_rect.topleft)
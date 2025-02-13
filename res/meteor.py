import pygame
from res.constants import *
import random


class Meteor(pygame.sprite.Sprite):
    def __init__(self, mob_images):
        super().__init__()
        size = random.randint(20, 50)
        self.image = pygame.transform.scale(random.choice(mob_images), (size, size))
        self.rect = self.image.get_rect()
        self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.top = -10
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(1, 7)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # if self.rect.right >= WIDTH + 30 or self.rect.left <= -30 or self.rect.bottom >= HEIGHT + 30:
        #     self.rect.centerx = random.randint(0, WIDTH)
        #     self.rect.top = -10

        if self.rect.top > HEIGHT:
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.top = -10
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(4, 13)


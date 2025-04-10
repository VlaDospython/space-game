import pygame
from constants import HEIGHT
import random


class AidKit(pygame.sprite.Sprite):
    def __init__(self, aidkit_img):
        super().__init__()
        self.image = pygame.transform.scale(aidkit_img, (60, 57))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, HEIGHT)
        self.rect.y = 0
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

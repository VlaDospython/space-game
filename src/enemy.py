import pygame
from src.constants import *
import random
from enemy_rocket import Rocket


class Enemy(pygame.sprite.Sprite):
    def __init__(self, context):
        super().__init__()
        self.image = context.get_surface()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, HEIGHT)
        self.rect.top = 0
        self.speedx = random.randint(-5, 5)
        self.speedy = random.randint(-1, 1)
        self.lives = 3
        self.dead = False

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # self.speedy = random.randint(-1, 1)

        if self.rect.x <= 0:
            self.speedx = random.randint(1, 5)
        elif self.rect.right > WIDTH:
            self.speedx = random.randint(-5, -1)

        if self.rect.y <= 0:
            self.speedy = 1
        elif self.rect.y >= 50:
            self.speedy = -1

    def launch_rocket(self, target, rocket_group, explosion_images, meteors_group):
        rocket = Rocket(self.rect.centerx, self.rect.bottom, target, explosion_images, meteors_group)
        rocket_group.add(rocket)





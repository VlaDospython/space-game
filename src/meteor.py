import pygame
from src.constants import *
import random


class Meteor(pygame.sprite.Sprite):
    all_meteors = []

    def __init__(self, mob_images):
        super().__init__()
        Meteor.all_meteors.append(self)
        size = random.randint(20, 50)
        self.image = pygame.transform.scale(random.choice(mob_images), (size, size))
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.top = -10
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(1, 7)
        self.last_update = pygame.time.get_ticks()
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)

    def rotate(self):
        self.rotation = (self.rotation + self.rotation_speed) % 360
        new_image = pygame.transform.rotate(self.image_orig, self.rotation)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    @classmethod
    def rotate_all(cls):
        for meteor in cls.all_meteors:
            meteor.rotate()

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


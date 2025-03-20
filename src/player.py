import pygame
from src.constants import *
from src.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, context):
        super().__init__()
        self.image = context.get_surface()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.lives = 3

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10

        self.rect.x += self.speedx

    def shoot(self):
        from src.main import bullets
        bullet = Bullet(self.rect.centerx, self.rect.top, RED)
        bullets.add(bullet)

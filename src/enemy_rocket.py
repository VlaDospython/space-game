import pygame
from constants import *


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_player, explosion_images, meteors_group):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.target = target_player
        self.meteors_group = meteors_group
        self.explosion_images = explosion_images
        self.exploded = False

        target_center = self.target.rect.center
        dx = target_center[0] - x
        dy = target_center[1] - y

        distance = (dx**2 + dy**2) ** 0.5
        self.speedx = dx / distance * 2
        self.speedy = dy / distance * 2

    def update(self):
        if not self.exploded:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery

            direction = pygame.math.Vector2(dx, dy)
            if direction.length() != 0:
                direction = direction.normalize()

            self.speedy += 0.15

            self.rect.x += direction.x * 10
            self.rect.y += self.speedy

            if pygame.math.Vector2(self.rect.center).distance_to(self.target.rect.center) < 30:
                self.explode()
        else:
            self.kill()

    def explode(self):
        self.exploded = True

        # explosion = Explosion(center=self.rect.center, explosion_images=self.explosion_images)
        # all_sprites.add(explosion)

        for meteor in self.meteors_group:
            dist = pygame.math.Vector2(meteor.rect.center).distance_to(self.rect.center)
            if dist < EXPLOSION_RADIUS:
                meteor.kill()
                self.target.kill()
                pygame.quit()

        self.kill()


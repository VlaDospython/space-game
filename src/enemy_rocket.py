import pygame
from constants import *
import math


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_player, explosion_images, meteors_group, rocket_img):
        super().__init__()
        self.original_image = pygame.transform.smoothscale(rocket_img, (65, 35))
        self.original_image = pygame.transform.rotate(self.original_image, -90)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.target = target_player
        self.meteors_group = meteors_group
        self.explosion_images = explosion_images
        self.exploded = False
        self.rotation = 0

        target_center = self.target.rect.center
        dx = target_center[0] - x
        dy = target_center[1] - y

        distance = (dx**2 + dy**2) ** 0.5
        self.speedx = dx / distance * 2
        self.speedy = dy / distance * 2

    def rotate(self, dx, dy):
        angle_rad = math.atan2(dx, dy)  # Повертає кут у радіанах
        angle_deg = math.degrees(angle_rad)  # Перетворюємо на градуси

        self.rotation = angle_deg

        new_image = pygame.transform.rotate(self.original_image, self.rotation)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect(center=old_center)

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

            self.rotate(dx, dy)

            if pygame.math.Vector2(self.rect.center).distance_to(self.target.rect.center) < 30:
                self.explode()
        else:
            self.kill()

    def explode(self):
        from meteor import Meteor

        self.exploded = True
        meteor = pygame.image.load(METEOR_IMG)
        mob_images = [meteor]

        # explosion = Explosion(center=self.rect.center, explosion_images=self.explosion_images)
        # all_sprites.add(explosion)

        for meteor in self.meteors_group:
            dist = pygame.math.Vector2(meteor.rect.center).distance_to(self.rect.center)
            if dist < EXPLOSION_RADIUS:
                meteor.kill()
                self.meteors_group.add(Meteor(mob_images))
                # self.target.kill()
                self.target.dead = True
                self.target.lives = 0
                # del self.target

        del self


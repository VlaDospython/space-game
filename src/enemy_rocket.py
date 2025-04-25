import pygame


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_rect, explosion_images, meteors_group):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.target = target_rect
        self.meteors_group = meteors_group
        self.explosion_images = explosion_images
        self.exploded = False

        dx = self.target.centerx - x
        dy = self.target.centery - y
        distance = (dx**2 + dy**2) ** 0.5
        self.speedx = dx / distance * 2
        self.speedy = dy / distance * 2

    def update(self):
        if not self.exploded:
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.rect.colliderect(self.target.inflate(30, 30)):
                self.explode()
        else:
            self.kill()

    def explode(self):
        self.exploded = True

        # explosion = Explosion(center=self.rect.center, explosion_images=self.explosion_images)
        # all_sprites.add(explosion)

        explosion_radius = 100
        for meteor in self.meteors_group:
            if pygame.math.Vector2(meteor.rect.center).distance_to(self.rect.center) < explosion_radius:
                meteor.kill()

        self.kill()


import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, context):
        super().__init__()
        # self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image = context.get_surface()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.bottom < 0:
            self.kill()

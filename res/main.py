import pygame
import random
import psutil # Використання пам’яті всього процесу
import os

WIDTH = 800
HEIGHT = 600
FPS = 30
x = 400
y = 300
img = pygame.image.load("../src/images/stars_space_galaxy_117958_800x600.jpg")
meteor = pygame.image.load("../src/images/meteorite3.png")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My game')
pygame.mixer.init()
running = True
clock = pygame.time.Clock()
mob_images = [meteor]


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

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


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

process = psutil.Process(os.getpid())

meteors = pygame.sprite.Group()

# **Додавання метеоритів у групу
for _ in range(random.randint(15, 30)):
    meteors.add(Meteor())


while running:
    clock.tick(FPS)
    print(f"Використано пам'яті: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Заливка екрану чорним кольором
    screen.blit(img, (0, 0))
    meteors.update()
    meteors.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()  # Оновлюємо весь екран

pygame.quit()


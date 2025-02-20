import pygame
import random
import psutil  # Використання пам’яті всього процесу
import os
from src.constants import *
from src.player import Player
from src.meteor import Meteor

# Load images
img = pygame.image.load(BG_IMG)
meteor = pygame.image.load(METEOR_IMG)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
pygame.mixer.init()
running = True
clock = pygame.time.Clock()
mob_images = [meteor]


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

process = psutil.Process(os.getpid())
total_memory_mb = psutil.virtual_memory().total / (1024 * 1024)

meteors = pygame.sprite.Group()

# **Додавання метеоритів у групу
for _ in range(random.randint(15, 30)):
    meteors.add(Meteor(mob_images))


while running:
    clock.tick(FPS)
    print(f"Використано пам'яті: {process.memory_info().rss / 1024 / 1024:.2f}/{total_memory_mb:.2f} MB")
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


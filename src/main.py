import pygame
import random
import psutil  # Використання пам’яті всього процесу
import os
from src.constants import *
from src.player import Player
from src.meteor import Meteor
from abc import ABC, abstractmethod


class Context:
    def set_strategy(self, strat):
        self.strategy = strat

    def get_surface(self):
        return self.strategy.get_surface()


class Strategy(ABC):
    @abstractmethod
    def get_surface(self):
        pass


class SimpleImage(Strategy):
    def __init__(self):
        self.image = pygame.Surface((25, 40))
        self.image.fill(RED)

    def get_surface(self):
        return self.image


class PhotoImage(Strategy):
    def __init__(self, player_image):
        self.image = pygame.transform.scale(player_image, (36, 42))
        self.image.set_colorkey(BLACK)

    def get_surface(self):
        return self.image


# Load images
img = pygame.image.load(BG_IMG)
meteor = pygame.image.load(METEOR_IMG)
ship = pygame.image.load(SHIP)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
pygame.mixer.init()
running = True
clock = pygame.time.Clock()
mob_images = [meteor]

c = Context()
c.set_strategy(PhotoImage(player_image=ship))

all_sprites = pygame.sprite.Group()
player = Player(context=c)
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

    if process.memory_info().rss / 1024 / 1024 > 200:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Перевірка на зіткнення з метеорами
    hits = pygame.sprite.spritecollide(player, meteors, True)
    if hits:
        running = False

    # Оновлення стану ігрових об'єктів
    meteors.update()
    all_sprites.update()
    pygame.display.update()  # Оновлюємо весь екран
    Meteor.rotate_all()

    # Рендеринг
    screen.fill((0, 0, 0))  # Заливка екрану чорним кольором
    screen.blit(img, (0, 0))
    meteors.draw(screen)
    all_sprites.draw(screen)

pygame.quit()


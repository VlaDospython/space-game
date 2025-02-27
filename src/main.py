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


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(heart, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def spawn_hearts():
    player_lives = player.lives
    pos_x = 10
    for j in range(player_lives):
        pos_x += 20
        heart = Heart(pos_x, 10)
        hearts.append(heart)
        if isinstance(heart, Heart):
            all_sprites.add(heart)


# Load images
img = pygame.image.load(BG_IMG)
meteor = pygame.image.load(METEOR_IMG)
ship = pygame.image.load(SHIP)
heart = pygame.image.load(HEART)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
pygame.mixer.init()
running = True
clock = pygame.time.Clock()
mob_images = [meteor]
hearts = []

c = Context()
c.set_strategy(PhotoImage(player_image=ship))

all_sprites = pygame.sprite.Group()
player = Player(context=c)
all_sprites.add(player)
all_sprites.add(hearts)

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
        player.lives -= 1
        all_sprites.remove(hearts)
        hearts = []
        spawn_hearts()

    # Перевірка кількості життів
    if player.lives == 0:
        running = False

    # Оновлення стану ігрових об'єктів
    meteors.update()
    all_sprites.update()
    pygame.display.update()  # Оновлюємо весь екран
    Meteor.rotate_all()
    spawn_hearts()

    # Рендеринг
    screen.fill((0, 0, 0))  # Заливка екрану чорним кольором
    screen.blit(img, (0, 0))
    meteors.draw(screen)
    all_sprites.draw(screen)

pygame.quit()


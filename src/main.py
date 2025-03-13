import pygame
import random
import psutil  # Використання пам’яті всього процесу
import os
from src.constants import *
from src.player import Player
from src.meteor import Meteor
from src.heart import Heart
# from src.image_strategy.Strategy import Strategy
# from src.image_strategy.SimpleImage import SimpleImage
from src.image_strategy.PhotoImage import PhotoImage
from src.image_strategy.context import Context


# Load images
img = pygame.image.load(BG_IMG)
meteor = pygame.image.load(METEOR_IMG)
ship = pygame.image.load(SHIP)
heart_img = pygame.image.load(HEART)
pygame.init()


def spawn_hearts():
    player_lives = player.lives
    pos_x = 10
    for j in range(player_lives):
        pos_x += 20
        heart = Heart(pos_x, 10, heart_img)
        hearts.append(heart)
        if isinstance(heart, Heart):
            all_sprites.add(heart)


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


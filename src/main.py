import pygame
import random
import psutil  # Використання пам’яті всього процесу
import os
from src.constants import *
from src.player import Player
from src.bullet import Bullet
from src.meteor import Meteor
from src.heart import Heart
from src.Big_meteor import Big_Meteor
from src.image_strategy.PhotoImage import PhotoImage
from src.image_strategy.SimpleImage import SimpleImage
from src.image_strategy.context import Context
from medicine import AidKit
from enemy import Enemy

# Load images
img = pygame.image.load(BG_IMG)
meteor = pygame.image.load(METEOR_IMG)
ship = pygame.image.load(SHIP)
heart_img = pygame.image.load(HEART)
aidkit_img = pygame.image.load(AIDKIT_IMG)
enemy_img = pygame.image.load(ENEMY_IMG)
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


def play_sound(sound_: str, number_of_channel: int):
    channel = pygame.mixer.Channel(number_of_channel)
    channel.set_volume(0.1)
    channel.play(pygame.mixer.Sound(sound_))


def shoot():
    global current_time
    current_time = pygame.time.get_ticks()
    bullet = Bullet(player.rect.centerx, player.rect.top, b)
    bullets.add(bullet)
    play_sound(BULLET_SOUND_3, 1)


def spawn_big_meteor():
    global big_meteor_current_time
    big_meteor_current_time = pygame.time.get_ticks()
    big_meteors.add(Big_Meteor(mob_images))


def spawn_aidkit():
    global aidkit_current_time
    aidkit_current_time = pygame.time.get_ticks()
    aidkits.add(AidKit(aidkit_img))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)
pygame.mixer.init()
bg_music = pygame.mixer.Sound(BG_MUSIC)
bg_music.set_volume(0.1)
bg_music.play()
running = True
clock = pygame.time.Clock()
mob_images = [meteor]
hearts = []

c = Context()
c.set_strategy(PhotoImage(player_image=ship))
b = Context()
b.set_strategy(SimpleImage(size=(5, 10), color=RED))
enemy_context = Context()
enemy_context.set_strategy(PhotoImage(player_image=enemy_img))

all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
big_meteors = pygame.sprite.Group()
aidkits = pygame.sprite.Group()

player = Player(context=c)
enemy = Enemy(context=enemy_context)
all_sprites.add(player)
all_sprites.add(hearts)
all_sprites.add(enemy)

process = psutil.Process(os.getpid())
total_memory_mb = psutil.virtual_memory().total / (1024 * 1024)


# **Додавання метеоритів у групу
for _ in range(random.randint(15, 30)):
    meteors.add(Meteor(mob_images))

current_time = pygame.time.get_ticks()
big_meteor_current_time = pygame.time.get_ticks()
aidkit_current_time = pygame.time.get_ticks()

while running:
    clock.tick(FPS)
    # print(f"Використано пам'яті: {process.memory_info().rss / 1024 / 1024:.2f}/{total_memory_mb:.2f} MB")

    if process.memory_info().rss / 1024 / 1024 > 200:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE]:
        if pygame.time.get_ticks() - current_time >= SHOOT_DELAY:
            shoot()

    # Перевірка на зіткнення з метеорами
    hits = pygame.sprite.spritecollide(player, meteors, True)
    if hits:
        player.lives -= 1
        all_sprites.remove(hearts)
        hearts = []
        spawn_hearts()
        play_sound(EXPLOSION_SOUND, 2)

    # Перевірка на зіткнення з великими метеорами
    hits = pygame.sprite.spritecollide(player, big_meteors, True)
    if hits:
        player.kill()
        running = False

    # Перевірка кількості життів
    if player.lives == 0:
        running = False

    bullets_hits = pygame.sprite.groupcollide(groupa=meteors, groupb=bullets, dokilla=True, dokillb=True)
    for hit in bullets_hits:
        print(hit)

        meteors.add(Meteor(mob_images))

    big_bullets_hits = pygame.sprite.groupcollide(groupa=big_meteors, groupb=bullets, dokilla=False, dokillb=True)
    for hit in big_bullets_hits:
        hit.lives -= 1
        print(hit.lives)

    aidkit_hits = pygame.sprite.spritecollide(player, aidkits, True)
    for hit in aidkit_hits:
        player.lives += 1
        all_sprites.remove(hearts)
        hearts = []
        spawn_hearts()
        play_sound(AIDKIT_SOUND, 3)

    if pygame.time.get_ticks() - big_meteor_current_time >= BIG_METEOR_SPAWN_DELAY:
        spawn_big_meteor()

    if pygame.time.get_ticks() - aidkit_current_time >= AIDKIT_SPAWN_DELAY:
        spawn_aidkit()

    # Оновлення стану ігрових об'єктів
    bullets.update()
    meteors.update()
    big_meteors.update()
    all_sprites.update()
    aidkits.update()
    pygame.display.update()  # Оновлюємо весь екран
    Meteor.rotate_all()
    spawn_hearts()

    # Рендеринг
    screen.fill((0, 0, 0))  # Заливка екрану чорним кольором
    screen.blit(img, (0, 0))
    all_sprites.draw(screen)
    meteors.draw(screen)
    big_meteors.draw(screen)
    bullets.draw(screen)
    aidkits.draw(screen)

pygame.quit()

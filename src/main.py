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
from explosion import Explosion

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


def play_sound(sound_: str, number_of_channel: int, volume: float):
    channel = pygame.mixer.Channel(number_of_channel)
    channel.set_volume(volume)
    channel.play(pygame.mixer.Sound(sound_))


def shoot():
    global current_time
    current_time = pygame.time.get_ticks()
    bullet = Bullet(player.rect.centerx, player.rect.top, b)
    bullets.add(bullet)
    play_sound(BULLET_SOUND_3, 1, volume=0.1)


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
shake_offset = [0, 0]
shake_duration = 0
shake_intensity = 0
shake_start_time = 0

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
explosions = pygame.sprite.Group()

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


def load_explosion_images(size_1: int, size_2: int):
    images = []
    for i in range(9):
        path = os.path.join(EXPLOSION_FOLDER, f"00{i}.png")
        frame = pygame.image.load(path).convert_alpha()
        frame = pygame.transform.scale(frame, (size_1, size_2))
        images.append(frame)
    return images


explosion_images = load_explosion_images(90, 90)


def start_screen_shake(intensity, duration):
    global shake_duration, shake_intensity, shake_start_time
    shake_intensity = intensity
    shake_duration = duration
    shake_start_time = pygame.time.get_ticks()


def update_screen_shake():
    global shake_offset
    if pygame.time.get_ticks() - shake_start_time < shake_duration:
        shake_offset[0] = random.randint(-shake_intensity, shake_intensity)
        shake_offset[1] = random.randint(-shake_intensity, shake_intensity)
    else:
        shake_offset = [0, 0]


while running:
    clock.tick(FPS)
    print(f"Використано пам'яті: {process.memory_info().rss / 1024 / 1024:.2f}/{total_memory_mb:.2f} MB")

    if process.memory_info().rss / 1024 / 1024 > 200:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE]:
        if pygame.time.get_ticks() - current_time >= SHOOT_DELAY:
            shoot()

    # Перевірка на зіткнення гравця з метеорами
    hits = pygame.sprite.spritecollide(player, meteors, True)
    if hits:
        player.lives -= 1
        all_sprites.remove(hearts)
        hearts = []
        spawn_hearts()
        start_screen_shake(intensity=15, duration=700)
        for hit in hits:
            play_sound(SHUTTLE_EXPLOSION_SOUND, 4, volume=0.2)
            explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
            all_sprites.add(explosion)
            explosions.add(explosion)

    # Перевірка на зіткнення гравця з великими метеорами
    hits = pygame.sprite.spritecollide(player, big_meteors, True)
    if hits:
        explosion_images1 = load_explosion_images(164, 164)
        explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images1)
        all_sprites.add(explosion)
        explosions.add(explosion)
        play_sound(SHUTTLE_EXPLOSION_SOUND, 5, volume=0.2)
        player.kill()
        running = False

    # Перевірка кількості життів
    if player.lives <= 0:
        explosion_images1 = load_explosion_images(164, 164)
        explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images1)
        all_sprites.add(explosion)
        explosions.add(explosion)
        play_sound(SHUTTLE_EXPLOSION_SOUND, 5, volume=0.2)
        running = False

    # Перевірка на зіткнення куль з метеоритами
    bullets_hits = pygame.sprite.groupcollide(groupa=meteors, groupb=bullets, dokilla=True, dokillb=True)
    for hit in bullets_hits:
        explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
        all_sprites.add(explosion)
        explosions.add(explosion)
        meteors.add(Meteor(mob_images))
        play_sound(EXPLOSION_SOUND, 2, volume=0.1)

    # Перевірка на зіткнення куль з великими метеорами
    big_bullets_hits = pygame.sprite.groupcollide(groupa=big_meteors, groupb=bullets, dokilla=False, dokillb=True)
    for hit in big_bullets_hits:
        hit.lives -= 1
        print(hit.lives)
        explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
        all_sprites.add(explosion)
        explosions.add(explosion)
        play_sound(EXPLOSION_SOUND, 2, volume=0.1)

        if hit.lives <= 0:
            explosion_images_ = load_explosion_images(264, 264)
            explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images_)
            all_sprites.add(explosion)
            explosions.add(explosion)
            play_sound(BIG_EXPLOSION_SOUND, 5, volume=0.7)

    # Перевірка на зіткнення гравця з аптечками
    aidkit_hits = pygame.sprite.spritecollide(player, aidkits, True)
    for hit in aidkit_hits:
        player.lives += 1
        all_sprites.remove(hearts)
        hearts = []
        spawn_hearts()
        play_sound(AIDKIT_SOUND, 3, volume=1)

    # Перевірка на зіткнення ворога з кулями
    bullets_hits_to_enemy = pygame.sprite.spritecollide(enemy, bullets, True)
    for hit in bullets_hits_to_enemy:
        explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
        all_sprites.add(explosion)
        explosions.add(explosion)
        enemy.lives -= 1
        play_sound(EXPLOSION_SOUND, 2, volume=0.1)

    # Перевірка кількості життів ворога
    if enemy.lives <= 0 and not enemy.dead:
        explosion_images1 = load_explosion_images(164, 164)
        explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images1)
        all_sprites.add(explosion)
        explosions.add(explosion)
        enemy.dead = True
        # TODO: delete enemy from memory after death
        all_sprites.remove(enemy)
        play_sound(SHUTTLE_EXPLOSION_SOUND, 5, volume=0.2)


    # Перевірка на зіткнення куль з аптечками
    aidkit_bullet_hits = pygame.sprite.groupcollide(bullets, aidkits, dokilla=True, dokillb=True)
    for hit in aidkit_bullet_hits:
        play_sound(EXPLOSION_SOUND, 2, volume=0.1)

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
    explosions.update()
    update_screen_shake()
    Meteor.rotate_all()
    spawn_hearts()

    # Рендеринг
    screen.fill((0, 0, 0))  # Заливка екрану чорним кольором
    screen.blit(img, shake_offset)
    all_sprites.draw(screen)
    meteors.draw(screen)
    big_meteors.draw(screen)
    bullets.draw(screen)
    aidkits.draw(screen)
    explosions.draw(screen)

pygame.quit()

import pygame
import random
import psutil  # Використання пам’яті всього процесу
import os
import csv
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
from storage_strategy import *
# from enemy_rocket import Rocket


def main():
    def spawn_hearts():
        player_lives = player.lives
        pos_x = 10
        for j in range(player_lives):
            pos_x += 20
            heart = Heart(pos_x, 10, heart_img)
            hearts.append(heart)
            if isinstance(heart, Heart):
                all_sprites.add(heart)

    # def play_sound(sound_: str, number_of_channel: int, volume: float):
    #     channel = pygame.mixer.Channel(number_of_channel)
    #     channel.set_volume(volume)
    #     channel.play(pygame.mixer.Sound(sound_))

    def shoot():
        if not player.dead:
            nonlocal current_time
            current_time = pygame.time.get_ticks()
            bullet = Bullet(player.rect.centerx, player.rect.top, b)
            bullets.add(bullet)
            bullet_channel.play(pygame.mixer.Sound(BULLET_SOUND_3))

    def spawn_big_meteor():
        nonlocal big_meteor_current_time
        big_meteor_current_time = pygame.time.get_ticks()
        big_meteors.add(Big_Meteor(mob_images))

    def spawn_aidkit():
        nonlocal aidkit_current_time
        aidkit_current_time = pygame.time.get_ticks()
        aidkits.add(AidKit(aidkit_img))

    def load_explosion_images(size_1: int, size_2: int):
        images = []
        for i in range(9):
            path = os.path.join(EXPLOSION_FOLDER, f"00{i}.png")
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (size_1, size_2))
            images.append(frame)
        return images

    def start_screen_shake(intensity, duration):
        nonlocal shake_duration, shake_intensity, shake_start_time
        shake_intensity = intensity
        shake_duration = duration
        shake_start_time = pygame.time.get_ticks()

    def update_screen_shake():
        nonlocal shake_offset
        if pygame.time.get_ticks() - shake_start_time < shake_duration:
            shake_offset[0] = random.randint(-shake_intensity, shake_intensity)
            shake_offset[1] = random.randint(-shake_intensity, shake_intensity)
        else:
            shake_offset = [0, 0]

    def spawn_meteors(difficulty: int):
        # Додавання метеоритів у групу
        if difficulty == 1:
            for _ in range(random.randint(5, 10)):
                meteors.add(Meteor(mob_images))
        elif difficulty == 2:
            for _ in range(random.randint(10, 20)):
                meteors.add(Meteor(mob_images))
        elif difficulty == 3:
            for _ in range(random.randint(20, 40)):
                meteors.add(Meteor(mob_images))

    def draw_text(surf, text, color, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw_blinking_text(surf, text, color, size, x, y, interval_ms):
        """
        Blinks text at a specified interval. Uses draw_text inside itself
        """
        time_now = pygame.time.get_ticks()

        if (time_now // interval_ms) % 2 == 0:
            draw_text(surf, text, color, size, x, y)

    def draw_progress_bar(surf, x, y, width, height, progress, max_progress):
        pygame.draw.rect(surf, BLACK, (x, y, width, height), 2)

        fill_width = int((progress / max_progress) * width)
        pygame.draw.rect(surf, (0, 200, 0), (x + 1, y + 1, fill_width - 2, height - 2))

    def fly_player_up(player, speed):
        if player.rect.bottom > 0:
            player.rect.y -= speed

    def fly_player_down(player, speed):
        if player.rect.bottom > 0:
            player.rect.y += speed

    def reset_player_position():
        player.rect.centerx = WIDTH // 2
        player.rect.bottom = HEIGHT - 10
        player.speedx = 0
        player.speedy = 0

    def reset_variables():
        nonlocal game_state
        nonlocal progress_complete
        nonlocal progress
        nonlocal shoot_delay
        nonlocal score
        nonlocal level_index
        nonlocal score_saved
        nonlocal progress_started
        nonlocal progress_speed

        player.dead = False
        progress_complete = False
        score_saved = False
        progress_started = False
        player.lives = 3
        progress = 0
        shoot_delay = 115
        score = 0
        level_index = 0
        progress_speed = 0.1

        rockets = pygame.sprite.Group()
        bullets.empty()
        meteors.empty()
        big_meteors.empty()
        aidkits.empty()
        explosions.empty()
        all_sprites.empty()

        all_sprites.add(player)
        all_sprites.add(rockets)
        spawn_hearts()
        reset_player_position()

    def first_level_load():
        nonlocal game_state
        nonlocal level_index
        nonlocal best_score
        nonlocal progress_started
        nonlocal data_context

        game_state = 1
        level_index = 1

        best_score = data_context.load_data(level_index)
        progress_started = True
        spawn_meteors(1)

    def second_level_load():
        nonlocal game_state
        nonlocal level_index
        nonlocal best_score
        nonlocal progress_started
        nonlocal progress_speed
        nonlocal data_context

        game_state = 1
        level_index = 2
        progress_speed = 0.05
        best_score = data_context.load_data(level_index)
        progress_started = True
        spawn_meteors(2)

    def third_level_load():
        nonlocal shoot_delay
        nonlocal game_state
        nonlocal level_index
        nonlocal best_score
        nonlocal progress_started
        nonlocal data_context

        game_state = 1
        shoot_delay -= 40
        level_index = 3
        best_score = data_context.load_data(level_index)
        progress_started = True
        spawn_meteors(3)

    pygame.init()

    # Game and display init
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    pygame.mixer.init()

    # Sounds
    bullet_channel = pygame.mixer.Channel(1)
    explosion_channel = pygame.mixer.Channel(2)
    big_explosion_channel = pygame.mixer.Channel(3)
    aidkit_channel = pygame.mixer.Channel(4)
    background_channel = pygame.mixer.Channel(5)
    shuttle_explosion_channel = pygame.mixer.Channel(6)
    background_channel.play(pygame.mixer.Sound(BG_MUSIC))

    # Images
    img = pygame.image.load(BG_IMG)
    start_screen_img = pygame.image.load(START_SCREEN_BG_IMG)
    level_screen_img = pygame.image.load(LEVEL_SCREEN_BG_IMG)
    meteor = pygame.image.load(METEOR_IMG)
    ship = pygame.image.load(SHIP)
    heart_img = pygame.image.load(HEART)
    aidkit_img = pygame.image.load(AIDKIT_IMG)
    enemy_img = pygame.image.load(ENEMY_IMG)
    enemy_rocket_img = pygame.image.load((ENEMY_ROCKET_IMG))
    explosion_images = load_explosion_images(90, 90)
    mob_images = [meteor]
    hearts = []

    shake_offset = [0, 0]
    shake_duration = 0
    shake_intensity = 0
    shake_start_time = 0
    explosion_time = 0
    progress = 0
    shoot_delay = 115
    score = 0
    level_index = 0
    best_score = 0
    progress_speed = 0.1

    progress_complete = False
    jump_time = None
    score_saved = False
    progress_started = False

    c = Context()

    c.set_strategy(PhotoImage(player_image=ship))
    b = Context()
    b.set_strategy(SimpleImage(size=(5, 10), color=RED))
    enemy_context = Context()
    enemy_context.set_strategy(PhotoImage(player_image=enemy_img))
    data_context = DataContext(CsvStorage())

    all_sprites = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    big_meteors = pygame.sprite.Group()
    aidkits = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    rockets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = Player(context=c)

    enemy = Enemy(context=enemy_context)
    all_sprites.add(player)

    all_sprites.add(hearts)
    all_sprites.add(rockets)
    process = psutil.Process(os.getpid())

    total_memory_mb = psutil.virtual_memory().total / (1024 * 1024)

    current_time = pygame.time.get_ticks()

    big_meteor_current_time = pygame.time.get_ticks()
    aidkit_current_time = pygame.time.get_ticks()
    rocket_current_time = pygame.time.get_ticks()
    enemy_spawn_current_time = pygame.time.get_ticks()
    running = True

    # Loop and FPS control
    clock = pygame.time.Clock()

    def game_loop(hearts):
        nonlocal game_state
        nonlocal rocket_current_time
        nonlocal explosion_time
        nonlocal enemy_spawn_current_time
        nonlocal progress_complete
        nonlocal jump_time
        nonlocal progress
        nonlocal score
        nonlocal level_index
        nonlocal score_saved
        nonlocal best_score
        nonlocal progress_started
        nonlocal data_context

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_SPACE]:
            if pygame.time.get_ticks() - current_time >= shoot_delay:
                shoot()

        # Перевірка на зіткнення гравця з метеорами
        hits = pygame.sprite.spritecollide(player, meteors, True)
        if hits:
            player.lives -= 1
            score -= 20
            all_sprites.remove(hearts)
            hearts = []
            spawn_hearts()
            start_screen_shake(intensity=15, duration=700)
            for hit in hits:
                shuttle_explosion_channel.play(pygame.mixer.Sound(SHUTTLE_EXPLOSION_SOUND))
                explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
                all_sprites.add(explosion)
                explosions.add(explosion)

        # Перевірка на зіткнення гравця з великими метеорами
        hits = pygame.sprite.spritecollide(player, big_meteors, True)
        if hits:
            player.lives -= 3
            score -= 50
            all_sprites.remove(hearts)
            hearts = []
            spawn_hearts()
            start_screen_shake(intensity=15, duration=700)
            for hit in hits:
                explosion_images1 = load_explosion_images(164, 164)
                explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images1)
                all_sprites.add(explosion)
                explosions.add(explosion)
                shuttle_explosion_channel.play(pygame.mixer.Sound(SHUTTLE_EXPLOSION_SOUND))

        # Перевірка кількості життів
        if player.lives <= 0 and not player.dead:
            player.dead = True
            score -= 50
            explosion_time = pygame.time.get_ticks()

        if player.dead and explosion_time is not None:
            if not shuttle_explosion_channel.get_busy():
                shuttle_explosion_channel.play(pygame.mixer.Sound(SHUTTLE_EXPLOSION_SOUND))

            start_screen_shake(intensity=25, duration=800)
            explosion_images1 = load_explosion_images(164, 164)
            explosion = Explosion(center=player.rect.center, explosion_images=explosion_images1)
            all_sprites.add(explosion)
            explosions.add(explosion)
            fly_player_down(player, speed=2)

            if not score_saved:
                data_context.save_data(level_index, score)

                best_score = data_context.load_data(level_index)
                score_saved = True

            if pygame.time.get_ticks() - explosion_time >= PAUSE_AFTER_DEATH:
                print("Вибух")
                game_state = 0
                shuttle_explosion_channel.stop()
                player.dead = False
                return

        # Перевірка на зіткнення куль з метеоритами
        bullets_hits = pygame.sprite.groupcollide(groupa=meteors, groupb=bullets, dokilla=True, dokillb=True)
        if bullets_hits:
            score += 10
            for hit in bullets_hits:
                explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
                all_sprites.add(explosion)
                explosions.add(explosion)
                meteors.add(Meteor(mob_images))
                explosion_channel.play(pygame.mixer.Sound(EXPLOSION_SOUND))

        # Перевірка на зіткнення куль з великими метеорами
        big_bullets_hits = pygame.sprite.groupcollide(groupa=big_meteors, groupb=bullets, dokilla=False, dokillb=True)
        for hit in big_bullets_hits:
            hit.lives -= 1
            print(hit.lives)
            explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
            all_sprites.add(explosion)
            explosions.add(explosion)
            explosion_channel.play(pygame.mixer.Sound(EXPLOSION_SOUND))

            if hit.lives <= 0:
                explosion_images_ = load_explosion_images(264, 264)
                explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images_)
                all_sprites.add(explosion)
                explosions.add(explosion)
                score += 50
            big_explosion_channel.play(pygame.mixer.Sound(BIG_EXPLOSION_SOUND))

        # Перевірка на зіткнення гравця з аптечками
        aidkit_hits = pygame.sprite.spritecollide(player, aidkits, True)
        for hit in aidkit_hits:
            player.lives += 1
            score += 10
            all_sprites.remove(hearts)
            hearts = []
            spawn_hearts()
            aidkit_channel.play(pygame.mixer.Sound(AIDKIT_SOUND))

        # Перевірка на зіткнення ворога з кулями
        bullets_hits_to_enemy = pygame.sprite.spritecollide(enemy, bullets, True)
        for hit in bullets_hits_to_enemy:
            explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images)
            all_sprites.add(explosion)
            explosions.add(explosion)
            enemy.lives -= 1
            print(enemy.lives, "enemy")
            explosion_channel.play(pygame.mixer.Sound(EXPLOSION_SOUND))

        # Перевірка кількості життів ворога
        if enemy.lives <= 0 and not enemy.dead:
            explosion_images1 = load_explosion_images(164, 164)
            explosion = Explosion(center=hit.rect.center, explosion_images=explosion_images1)
            all_sprites.add(explosion)
            explosions.add(explosion)
            enemy.dead = True
            score += 100

            # TODO: delete enemy from memory after death
            all_sprites.remove(enemy)
            shuttle_explosion_channel.play(pygame.mixer.Sound(SHUTTLE_EXPLOSION_SOUND))

            enemy_spawn_current_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - big_meteor_current_time >= BIG_METEOR_SPAWN_DELAY:
            spawn_big_meteor()

        if pygame.time.get_ticks() - aidkit_current_time >= AIDKIT_SPAWN_DELAY:
            spawn_aidkit()

        if pygame.time.get_ticks() - rocket_current_time >= ROCKET_SPAWN_DELAY and enemy in all_sprites:
            enemy.launch_rocket(player, rockets, explosion_images, meteors, enemy_rocket_img)
            rocket_current_time = pygame.time.get_ticks()

        # print(pygame.time.get_ticks(), enemy_spawn_current_time, pygame.time.get_ticks() - enemy_spawn_current_time)
        if pygame.time.get_ticks() - enemy_spawn_current_time >= ENEMY_SPAWN_DELAY and enemy.dead:
            all_sprites.add(enemy)
            enemy.lives = Enemy.max_lives
            enemy.dead = False
            enemy_spawn_current_time = pygame.time.get_ticks()
            rocket_current_time = pygame.time.get_ticks()

        if progress >= MAX_PROGRESS and not progress_complete:
            jump_time = pygame.time.get_ticks()
            progress_complete = True
            score += 100

        if progress_complete:
            progress = 100
            draw_blinking_text(screen, "CLEAR THE WAY", ORANGE, 65, WIDTH / 2, HEIGHT - 550, 150)

            if pygame.time.get_ticks() - jump_time >= PAUSE_BEFORE_JUMP:
                fly_player_up(player, speed=10)

        if player.rect.bottom <= 0:
            game_state = 0
            return

        # Оновлення стану ігрових об'єктів
        bullets.update()
        meteors.update()
        big_meteors.update()
        all_sprites.update()
        aidkits.update()
        pygame.display.update()  # Оновлюємо весь екран
        explosions.update()
        rockets.update()
        update_screen_shake()
        Meteor.rotate_all()
        spawn_hearts()

        # Рендеринг
        screen.fill((0, 0, 0))  # Заливка екрану чорним кольором
        screen.blit(img, (0, 0))
        screen.blit(img, shake_offset)
        all_sprites.draw(screen)
        meteors.draw(screen)
        big_meteors.draw(screen)
        bullets.draw(screen)
        aidkits.draw(screen)
        explosions.draw(screen)
        rockets.draw(screen)
        draw_progress_bar(screen, WIDTH / 2 + 90, 7, 300, 25, progress, MAX_PROGRESS)
        draw_text(screen, f"Score: {score}", WHITE, 30, WIDTH - (WIDTH - 80), 40)
        draw_text(screen, f"Best: {best_score}", WHITE, 30, WIDTH - (WIDTH - 80), 70)

    def start_screen():
        # Рендеринг
        screen.blit(start_screen_img, (0, 0))
        draw_text(screen, "Space Game", WHITE, 80, WIDTH / 2, HEIGHT / 2 - 150)
        draw_blinking_text(screen, "press <Enter> to choose level", WHITE, 35, WIDTH / 2, HEIGHT - 80, 350)
        pygame.display.flip()

    def level_screen():
        # Рендеринг
        screen.blit(level_screen_img, (0, 0))
        draw_text(screen, "Choose level:", WHITE, 65, WIDTH / 2 - 200, HEIGHT / 2 - 200)
        draw_blinking_text(screen, "Press the key on the keyboard according to the level number to start", WHITE, 32,
                           WIDTH / 2, HEIGHT - 80, 750)

        draw_text(screen, "1. First level", WHITE, 55, WIDTH / 2 - 210, HEIGHT - 400)
        draw_text(screen, "2. Second level", WHITE, 55, WIDTH / 2 - 182, HEIGHT - 300)
        draw_text(screen, "3. Third level", WHITE, 55, WIDTH / 2 - 200, HEIGHT - 200)
        pygame.display.flip()

    game_state = 0

    # 0: start screen
    # 1: game loop
    # 2: level screen

    while running:
        clock.tick(FPS)
        print(f"Використано пам'яті: {process.memory_info().rss / 1024 / 1024:.2f}/{total_memory_mb:.2f} MB")
        if progress_started:
            progress += progress_speed

        if process.memory_info().rss / 1024 / 1024 > 300:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_state == 0:
                    game_state = 2
                    reset_variables()
                if event.key == pygame.K_1 and game_state == 2:
                    first_level_load()
                if event.key == pygame.K_2 and game_state == 2:
                    second_level_load()
                if event.key == pygame.K_3 and game_state == 2:
                    third_level_load()

        if game_state == 0:
            start_screen()

        if game_state == 1:
            game_loop(hearts)

        if game_state == 2:
            level_screen()


if __name__ == '__main__':
    main()

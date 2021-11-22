import sys

from time import sleep

import pygame

from bullet import Bullet

from alien import Alien

import json

def update_screen(ai_settings, screen, stats, star, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран."""
    # При каждом проходе цикла перерисовывается экран.
    screen.fill(ai_settings.bg_color)

    star.blitme() # Используется для вывода изоражения одного рисунка, в качестве фонового
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Вывод счета
    sb.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets):
    """Реагирует на нажатие клавиш."""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_UP:
        ship.moving_top = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

        # Код согласно задания 14-1
    elif event.key == pygame.K_p:
        stats.game_active = True
        if stats.game_active:
            # Сбро игровых настроек.
            ai_settings.initialize_dynamic_settings()
            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

            stats.reset_stats()
            stats.game_active = True

            # Очитска списков пришельцев и пуль.
            aliens.empty()
            bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            create_fleet(ai_settings, screen, ship, aliens)

            # Перемещение корабля в центр нижнего края экрана
            ship.center_ship()

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_UP:
        ship.moving_top = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускаетновую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Сбро игровых настроек.
        ai_settings.initialize_dynamic_settings()

        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        # Сброс изображений счетов и уровня.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Очитска списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)

        # Перемещение корабля в центр нижнего края экрана
        ship.center_ship()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()

    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обраотка коллизий пуль с пришельцами."""
    # Удаление пуль и пришельцев, участвующих в коллизиях.
    colisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if colisions:
        for aliens in colisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:

        # Уничтожение существующих пуль .
        bullets.empty()
        ai_settings.increase_speed()

        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()

        # Создание нового флота
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullets(ai_settings, screen, ship, bullets):
    """Выпускает пули, если максимум еще не достигнут."""

    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляем количество пришельцев в ряду"""

    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцeв."""

    #  Создание пришельца и размещение его в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающих на экране."""

    avialable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avialable_space_y / (2 * alien_height))
    return number_rows

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""

    if stats.ships_left > 0:

        # Уменьшение ships_left.
        stats.ships_left -= 1

        # Обновление игровой информации.
        sb.prep_ships()

        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # происходит то же,что при столкновении с кораблем.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проврка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
        break

def change_fleet_direction(ai_settings, aliens):
    """Отпускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_high_score(stats, sb):
    """Проверяет, появился ли новый уровень."""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        filename = 'high_score.json'
        with open(filename, 'w') as f_obj:
            json.dump(stats.score, f_obj)
        sb.prep_high_score()

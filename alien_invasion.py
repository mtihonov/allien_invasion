import pygame

from settings import Settings

from game_stats import GameStats

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from button import Button

from scoreboard import Scoreboard

from stars import Stars

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "play")

    # Создание корабля
    ship = Ship(ai_settings, screen)

    #Создание группы для хранения пуль
    bullets = Group()

    # Создание группы для храненияфлота пришельцев.
    aliens = Group()

    # Создание фоноого рисунка.
    star = Stars(screen, ai_settings)

    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)


    # Создание экземпляра для хранения игровой статистики.
    stats = GameStats(ai_settings)

    # Создание экземпляра для хранения игрового счета.
    sb = Scoreboard(ai_settings, screen, stats)

     # Запуск основного цикла игры.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, star, sb, ship, aliens, bullets, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

run_game()


import pygame

from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения и получение прямоугльника.
        self.image = pygame.image.load('images\ship.bmp.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.centerx = self. screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра корабля.
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.bottom)


        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_down = False

    def update(self):
        """Обновляет позицию корабля с учетом флагов."""
        # Обновляет атрибут center, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_top and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        # Обновление атрибута rect наосновании self.center.
        self.rect.centerx = self.center
        self.rect.bottom = self.centery

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.center = self.screen_rect.centerx
        self.centery = self. screen_rect.bottom

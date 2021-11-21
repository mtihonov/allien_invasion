import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, ai_settings, screen):
        """Инициализирует пришельца и задает начальную позицию."""
        super(Alien, self). __init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения пришельца и назначение арибута rect.
        self.image = pygame.image.load('images\\ufo.bmp.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляетсяв левом верхнм углу экрана.
        self.rect.x = self.rect.left
        self.rect.y = self.rect.top

        # Сохранение точной позиции пришельца.
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит пришельца в текущем положении."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Возвращает  True, если пришелец находится у края."""
        if self.rect.right >= self.ai_settings.alien_distance:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает пришельца влево или вправо."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

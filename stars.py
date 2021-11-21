import pygame

from pygame.sprite import Sprite # Сделан импорт, чтобы сделать группу звезд и вывести их на экран

class Stars(Sprite):

    """Создает фоновое изображение звезд в произвольных местах."""

    def __init__(self, screen, ai_settings):
        super(Stars, self).__init__()
        """Инициализирует фоновое изображение звезды."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения звезды и назначение арибута rect.
        self.image = pygame.image.load('images\\stars.bmp.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def blitme(self): # использовать для вывода одной картинки (например как фоновой)
        """Выводит звезду в текущем положении."""
        self.screen.blit(self.image, self.rect)
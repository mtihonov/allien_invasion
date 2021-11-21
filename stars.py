import pygame

from random import randint

from pygame.sprite import Sprite # Сделан импорт, чтобы сделать группу звезд и вывести их на экран

class Stars(Sprite):

    """Создает фоновое изображение звезд в произвольных местах."""

    def __init__(self, screen, ai_settings):
        super(Stars, self).__init__()
        """Инициализирует фоновое изображение звезды."""
        self.screen = screen
        self.ai_settings = ai_settings
        self.random_number_x = randint(10, 1350)
        self.random_number_y = randint(10, 700)

        # Загрузка изображения звезды и назначение арибута rect.
        self.image = pygame.image.load('images\\stars.bmp.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.random_number_x
        self.rect.y = self.random_number_y

        # Каждая новая звезда появляется в произвольном месте.

        self.rect.x = self.random_number_x
        self.rect.y = self.random_number_y

    #def blitme(self): # использовать для вывода одной картинки (например как фоновой)
      #  """Выводит звезду в текущем положении."""
       # self.screen.blit(self.image, self.rect)
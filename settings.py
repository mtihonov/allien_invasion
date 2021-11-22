class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1360
        self.screen_height = 710
        self.bg_color = (0, 0, 0)

        # Параметры пули
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Настройка пришельцев
        self.fleet_drop_speed = 10
        self.alien_distance = 300

        # Темп ускорения игры.
        self.speedup_scale = 1.1

        # Темпы роста стоимости пришельцев.
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Иницализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 1.0
        self.bullet_speed_factor = 2.0
        self.alien_speed_factor = 0.5

        # fleet_direction = 1 обзначает движение вправо; а -1 = влево.
        self.fleet_direction = 1

        # Подсчет очков.
        self.alien_points = 50

    def increase_speed(self):
        """Увеличиваетнастройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

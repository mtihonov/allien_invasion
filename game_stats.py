import json

class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_settings):
        """Инициализирует статистику."""
        self.ai_settings = ai_settings
        self.ships_limit = 3
        self.reset_stats()
        self.game_active = False

        # Рекорд не жолжен сбрасываться.
        self.high_score = []
        self.filename = 'high_score.json'
        try:
            with open(self.filename) as f_obj:
                self.high_score = json.load(f_obj)
        except FileNotFoundError:
            self.high_score = 0
            pass
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.ships_limit
        self.score = 0
        self.level = 1
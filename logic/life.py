import config


class LifeCounter:
    def __init__(self, lives=3):
        self.lives: int = lives

    def add(self):
        self.lives += 1

    def remove(self):
        self.lives -= 1
        if self.lives < 0:
            config.Settings.game_over = True

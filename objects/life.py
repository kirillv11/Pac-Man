import pyray
from config import Settings


class LifeDrawer:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.padding = 30
        image = pyray.load_image('./resources/image/health.png')
        self.texture = pyray.load_texture_from_image(image)
        pyray.unload_image(image)

    @staticmethod
    def decrease_lives():
        if Settings.life_counter.lives > 0:
            Settings.life_counter.lives -= 1

    def draw_lives(self, lives):
        for live in range(lives):
            pyray.draw_texture(self.texture, 20 +
                               (self.padding * live), 0, pyray.WHITE)

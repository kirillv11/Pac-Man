import pyray
from raylib import colors
import time
from config import Settings


class Seed:
    def __init__(self, cords):
        self.weight = 10
        self.cords = cords
        self.x = self.cords[0]
        self.y = self.cords[1]
        self.rect = pyray.Rectangle(self.x, self.y, 20, 20)
        self.dead = False
        self.show = True

    def die(self):
        self.dead = True
        Settings.death_seeds_count += 1
        if Settings.death_seeds_count >= 508:
            Settings.game_finished = True

    def draw(self):
        if not self.dead:
            pyray.draw_circle(self.cords[0] + 10,
                              self.cords[1] + 10, 3, colors.RAYWHITE)


class Energizer:
    def __init__(self, cords):
        self.weight = 50
        self.cords = cords
        self.x = self.cords[0]
        self.y = self.cords[1]
        self.rect = pyray.Rectangle(self.x, self.y, 20, 20)
        self.dead = False
        self.show = True

    def die(self):
        self.dead = True
        Settings.death_seeds_count += 1
        if Settings.death_seeds_count > 508:
            Settings.game_finished = True

    def draw(self):
        if not self.dead:
            pyray.draw_circle(self.cords[0] + 10,
                              self.cords[1] + 10, 5, colors.RAYWHITE)


class Cherry:
    def __init__(self, cords):
        self.weight = 100
        self.cords = cords
        self.x = self.cords[0]
        self.y = self.cords[1]
        self.radius = 10
        self.color = colors.RED
        self.show = False
        self.last_change = time.time()
        self.dead = False

    def init_texture(self):
        image_cherry = pyray.load_image('./resources/image/cherry.png')
        self.texture_cherry = pyray.load_texture_from_image(image_cherry)
        pyray.unload_image(image_cherry)

    def logic(self):
        if not Settings.game_stop:
            if not self.show and time.time() - self.last_change > 3:
                self.show = True
            elif self.show and time.time() - self.last_change > 8:
                self.show = False
                self.last_change = time.time()

    def draw(self):
        if not self.dead and self.show:
            pyray.draw_texture(self.texture_cherry,
                               self.x, self.y, pyray.WHITE)

    def die(self):
        self.dead = True
        Settings.death_seeds_count += 1
        if Settings.death_seeds_count > 508:
            Settings.game_finished = True

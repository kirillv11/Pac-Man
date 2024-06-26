import pyray
from raylib import colors
from typing import Dict
from config import Settings


class Cell:
    def __init__(self, cell_type: int, x: int, y: int, width: int = Settings.cell_size, height: int = Settings.cell_size):
        self.cell_type: int = cell_type
        self.width: int = width
        self.height: int = height
        self.color: pyray.Color = self.get_color()
        self.x = x
        self.y = y
        self.rect = pyray.Rectangle(self.x, self.y, self.width, self.height)
        image = pyray.load_image('./resources/image/portal.png')
        self.texture = pyray.load_texture_from_image(image)
        pyray.unload_image(image)

    def get_color(self):
        color: Dict[int, pyray.Color] = {
            0: colors.BLACK,  # пустое место
            1: colors.BLUE,  # стена
            2: colors.DARKBLUE,  # комната для призраков
            3: colors.YELLOW  # телепорт
        }
        return color.get(self.cell_type)

    def is_empty(self):
        return self.cell_type == 0

    def is_wall(self):
        return self.cell_type == 1

    def is_ghost_room(self):
        return self.cell_type == 2

    def is_teleport(self):
        return self.cell_type == 3

    def draw(self):
        if self.cell_type == 3:
            pyray.draw_texture(self.texture, int(self.rect.x),
                               int(self.rect.y), pyray.WHITE)
        else:
            pyray.draw_rectangle(int(self.rect.x), int(
                self.rect.y), self.width, self.height, self.color)

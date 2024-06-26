from cell import Cell
from objects.images.seed import Seed, Energizer, Cherry
from random import random


class FieldDrawer:
    def __init__(self, field, size):
        self.field = field
        self.size: int = size
        self.cells = list()

    def make_cells_list(self):
        self.cells.clear()
        for index, y in enumerate(self.field.field):
            for x in range(len(y)):
                if self.field.field[index][x] == "w":
                    new_cell = Cell(1, index * self.size, x * self.size)
                    self.cells.append(new_cell)
                if self.field.field[index][x] == "n":
                    new_cell = Cell(0, index * self.size, x * self.size)
                    self.cells.append(new_cell)
                if self.field.field[index][x] == "g":
                    new_cell = Cell(2, index * self.size, x * self.size)
                    self.cells.append(new_cell)
                if self.field.field[index][x] == "p":
                    new_cell = Cell(3, index * self.size, x * self.size)
                    self.cells.append(new_cell)
                if self.field.field[index][x] == "c":
                    new_cell = Cherry([index * self.size, x * self.size])
                    self.cells.append(new_cell)
                if self.field.field[index][x] == "s":
                    if random() > 0.01:
                        new_cell = Seed([index * self.size, x * self.size])
                    else:
                        new_cell = Energizer(
                            [index * self.size, x * self.size])
                    self.cells.append(new_cell)

    def draw(self):
        for cell in self.cells:
            cell.draw()
            if isinstance(cell, Cherry):
                cell.init_texture()
                cell.logic()

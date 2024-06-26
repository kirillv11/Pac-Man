import pyray
import random
import datetime


class Ghost:
    def __init__(self, x, y, color, start_direction):
        self.color = color
        self.sy = y
        self.sx = x
        self.x = x
        self.y = y
        self.direction = start_direction
        self.start_x = x
        self.start_y = y
        self.alive = True
        self.speed = 5
        self.dead_timer = datetime.datetime.now()
        self.texture = None
        self.texture_vulnerable = None
        self.pacman_direction = "none"

    def step(self, speed, direction):
        if direction == "up":
            self.y -= speed
        if direction == "down":
            self.y += speed
        if direction == "left":
            self.x -= speed
        if direction == "right":
            self.x += speed

    def init_image(self):
        image_vulnerable = pyray.load_image(
            './resources/image/ghost_vulnerable.png')
        self.texture_vulnerable = pyray.load_texture_from_image(
            image_vulnerable)
        pyray.unload_image(image_vulnerable)

        if self.color == 'red':
            image = pyray.load_image('./resources/image/ghost_red.png')
        elif self.color == 'blue':
            image = pyray.load_image('./resources/image/ghost_blue.png')
        elif self.color == 'pink':
            image = pyray.load_image('./resources/image/ghost_pink.png')
        elif self.color == 'orange':
            image = pyray.load_image('./resources/image/ghost_orange.png')

        self.texture = pyray.load_texture_from_image(image)
        pyray.unload_image(image)

    def draw(self, pacman):
        if self.alive:
            if pacman.energized:
                pyray.draw_texture(self.texture_vulnerable,
                                   self.x, self.y, pyray.WHITE)
            else:
                pyray.draw_texture(self.texture, self.x, self.y, pyray.WHITE)

    def check_walls(self, map, cell_size):
        x = self.x // cell_size
        y = self.y // cell_size
        r = []
        if map[x + 1][y] == "w" or map[x + 1][y] == "p":
            r.append(0)
        else:
            r.append(1)
        if map[x][y - 1] == "w" or map[x][y - 1] == "p":
            r.append(0)
        else:
            r.append(1)
        if map[x - 1][y] == "w" or map[x - 1][y] == "p":
            r.append(0)
        else:
            r.append(1)
        if map[x][y + 1] == "w" or map[x][y + 1] == "p":
            r.append(0)
        else:
            r.append(1)
        return r

    def check_cell(self, map, cell_size):
        x = self.x // cell_size
        y = self.y // cell_size
        return map[x][y]

    def collides_pacman(self, pacman):
        col = False
        x_delta = abs(self.x - pacman.x)
        y_delta = abs(self.y - pacman.y)
        if x_delta <= 5 and y_delta <= 5 and self.alive:
            col = True
        return col

    def revive(self):
        self.alive = True
        self.speed = 5
        self.x = self.sx
        self.y = self.sy

    def dead_timer_check(self):
        now = datetime.datetime.now()
        delta_time = now - self.dead_timer
        if not self.alive and delta_time >= datetime.timedelta(seconds=10):
            self.revive()

    def pacman_check(self, pacman):
        r = "right"
        gorizont = 0
        vertical = 0
        if self.x - pacman.x >= 0:
            gorizont = 1
        if self.y - pacman.y <= 0:
            vertical = 1
        if abs(self.x - pacman.x) > abs(self.y - pacman.y):
            if gorizont == 1:
                r = "left"
            else:
                r = "right"
        else:
            if vertical == 1:
                r = "down"
            else:
                r = "up"
        self.pacman_direction = r

    def logic(self, map, cell_size, pacman):

        if self.collides_pacman(pacman):
            if pacman.energized:
                self.alive = False
                self.dead_timer = datetime.datetime.now()
                pacman.score.add(200)

        if self.x % cell_size == 0 and self.y % cell_size == 0:
            self.pacman_check(pacman)
            if pacman.energized:
                self.speed = 4
            else:
                self.speed = 5
            walls = self.check_walls(map, cell_size)
            if sum(walls) == 2:
                if self.direction == "right":
                    if walls[0] == 1:
                        direct = "right"
                    elif walls[1] == 1:
                        direct = "up"
                    elif walls[3] == 1:
                        direct = "down"
                elif self.direction == "up":
                    if walls[0] == 1:
                        direct = "right"
                    elif walls[1] == 1:
                        direct = "up"
                    elif walls[2] == 1:
                        direct = "left"
                elif self.direction == "left":
                    if walls[1] == 1:
                        direct = "up"
                    elif walls[2] == 1:
                        direct = "left"
                    elif walls[3] == 1:
                        direct = "down"
                elif self.direction == "down":
                    if walls[0] == 1:
                        direct = "right"
                    elif walls[2] == 1:
                        direct = "left"
                    elif walls[3] == 1:
                        direct = "down"
                self.direction = direct
            elif sum(walls) == 1:
                if self.direction == "right":
                    self.direction = "left"
                elif self.direction == "up":
                    self.direction = "down"
                elif self.direction == "left":
                    self.direction = "right"
                elif self.direction == "down":
                    self.direction = "up"
            else:
                dir_list = ["right", "up", "left", "down"]
                if self.direction == "right":
                    dir_list.remove("left")
                elif self.direction == "up":
                    dir_list.remove("down")
                elif self.direction == "left":
                    dir_list.remove("right")
                elif self.direction == "down":
                    dir_list.remove("up")
                if walls[0] == 0 and "right" in dir_list:
                    dir_list.remove("right")
                elif walls[1] == 0 and "up" in dir_list:
                    dir_list.remove("up")
                elif walls[2] == 0 and "left" in dir_list:
                    dir_list.remove("left")
                elif walls[3] == 0 and "down" in dir_list:
                    dir_list.remove("down")
                if self.pacman_direction in dir_list and random.randint(0, 10) >= 4 and not pacman.energized:
                    self.direction = self.pacman_direction
                else:
                    self.direction = random.choice(dir_list)
        self.dead_timer_check()
        self.step(self.speed, self.direction)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

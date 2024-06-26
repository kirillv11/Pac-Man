import time

import pyray
import raylib
import datetime
from logic.score import ScoreCounter
import scenes.etc

class Pacman:
  def __init__(self, x, y, direction, sounds):
    self.start_y = y
    self.start_x = x
    self.x = x
    self.y = y
    self.sounds = sounds
    self.direction = 'none'
    self.score = ScoreCounter()
    self.future_direction = 'none'
    self.energized = False
    self.energized_time = datetime.datetime.now()
    self.speed = 4
    self.texture = None
    self.texture_right = None
    self.texture_left = None
    self.texture_bottom = None
    self.texture_forward = None
    self.last_eat = datetime.datetime.now()

  def check_collision(self, cell):
    return pyray.check_collision_recs(self.rect, cell.rect)

  def init_texture(self):
    image_pacman_right = pyray.load_image('./resources/image/pacman_right.png')
    image_pacman_left = pyray.load_image('./resources/image/pacman_left.png')
    image_pacman_bottom = pyray.load_image('./resources/image/pacman_bottom.png')
    image_pacman_forward = pyray.load_image('./resources/image/pacman_forward.png')

    self.texture_right = pyray.load_texture_from_image(image_pacman_right)
    self.texture_left = pyray.load_texture_from_image(image_pacman_left)
    self.texture_bottom = pyray.load_texture_from_image(image_pacman_bottom)
    self.texture_forward = pyray.load_texture_from_image(image_pacman_forward)
    self.texture = self.texture_forward

    pyray.unload_image(image_pacman_right)
    pyray.unload_image(image_pacman_left)
    pyray.unload_image(image_pacman_bottom)
    pyray.unload_image(image_pacman_forward)

  @staticmethod
  def walls_name(walls):
    r = []
    if walls[0] == 1:
      r.append("right")
    if walls[1] == 1:
      r.append("up")
    if walls[2] == 1:
      r.append("left")
    if walls[3] == 1:
      r.append("down")
    return r

  def draw(self):
    pyray.draw_texture(self.texture, self.x, self.y, pyray.WHITE)

  def step(self, direction, speed):
    if direction == "right":
      self.texture = self.texture_right
      self.x += speed
    if direction == "up":
      self.texture = self.texture_forward
      self.y -= speed
    if direction == "left":
      self.texture = self.texture_left
      self.x -= speed
    if direction == "down":
      self.texture = self.texture_bottom
      self.y += speed

  def check_walls(self, map, cell_size):
    x = self.x // cell_size
    y = self.y // cell_size
    r = []
    if map[x + 1][y] == "w" or map[x + 1][y] == "g":
      r.append(0)
    elif map[x + 1][y] == "p":
      r.append(2)
    else:
      r.append(1)
    if map[x][y - 1] == "w" or map[x][y - 1] == "g":
      r.append(0)
    elif map[x][y - 1] == "p":
      r.append(2)
    else:
      r.append(1)
    if map[x - 1][y] == "w" or map[x - 1][y] == "g":
      r.append(0)
    elif map[x - 1][y] == "p":
      r.append(2)
    else:
      r.append(1)
    if map[x][y + 1] == "w" or map[x][y + 1] == "g":
      r.append(0)
    elif map[x][y + 1] == "p":
      r.append(2)
    else:
      r.append(1)
    return r

  def seed_collision(self, x, y, cels):
    if not cels[x * 26 + y].dead and cels[x * 26 + y].show:
      self.score.add(cels[x * 26 + y].weight)
      if cels[x * 26 + y].weight == 50:
        self.energized = True
        pyray.play_sound(self.sounds.power_pellet)
        self.energized_time = datetime.datetime.now()
      cels[x * 26 + y].die()
      if datetime.datetime.now() - self.last_eat >= datetime.timedelta(seconds=0.25):
        pyray.play_sound(self.sounds.eat)
        self.last_eat = datetime.datetime.now()


  def check_energized(self):
    now = datetime.datetime.now()
    delta_time = now - self.energized_time
    if not pyray.is_sound_playing(self.sounds.power_pellet) and self.energized:
      pyray.play_sound(self.sounds.power_pellet)
    if self.energized and delta_time >= datetime.timedelta(seconds=8):
      self.energized = False
      pyray.pause_sound(self.sounds.power_pellet)

  def logic(self, map, cell_size, cels, ghosts, life_counter, game_scene_instance):
    self.check_energized()
    # проверка нажатых клавиш
    if pyray.is_key_down(raylib.KEY_D) or pyray.is_key_down(raylib.KEY_RIGHT):
      self.future_direction = "right"
    elif pyray.is_key_down(raylib.KEY_W) or pyray.is_key_down(raylib.KEY_UP):
      self.future_direction = "up"
    elif pyray.is_key_down(raylib.KEY_A) or pyray.is_key_down(raylib.KEY_LEFT):
      self.future_direction = "left"
    elif pyray.is_key_down(raylib.KEY_S) or pyray.is_key_down(raylib.KEY_DOWN):
      self.future_direction = "down"

    if self.collides_ghost(ghosts) and not self.energized:
      pyray.play_sound(self.sounds.death)
      scenes.etc.reset()
      life_counter.remove()
      game_scene_instance.start_time = time.time()

    if self.x % cell_size == 0 and self.y % cell_size == 0:
      if self.energized:
        self.speed = 5
      else:
        self.speed = 4
      self.seed_collision(self.x // cell_size, self.y // cell_size, cels)
      walls = self.check_walls(map, cell_size)
      if 2 in walls:
        if self.y == 20:
          self.y = 480
        elif self.y == 480:
          self.y = 20
      else:
        walls_named = self.walls_name(walls)
        if self.future_direction in walls_named:
          self.direction = self.future_direction
        if not self.direction in walls_named:
          self.direction = "none"
      self.seed_collision(self.x // cell_size, self.y // cell_size, cels)

    self.step(self.direction, self.speed)

  def collides_ghost(self, ghosts):  # проверка на столкновение с призраками (на вход идёт массив призраков)
    col = False
    x = self.x + 20
    y = self.y + 20
    for ghost in ghosts:
      if (x - ghost.x <= 20 + 20) and (y - ghost.y <= 20 + 20) and (
        x - ghost.x >= 0) and (y - ghost.y >= 0):
        col = True
    return col

  def reset(self):
    self.x = self.start_x
    self.y = self.start_y

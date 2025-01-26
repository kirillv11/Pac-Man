import time

import pyray
from raylib import colors
from objects.field import FieldDrawer
from objects.highscore import HighscoreTableDrawer
from objects.life import LifeDrawer
from objects.score import ScoreDrawer, RecalculableText
from config import Settings
from sys import exit
from objects.sounds import TurnCondition
from objects.random_names import Random_names


pause_memory = {
    "x": int,
    "y": int,
    "spaceX": 35,
    "spaceY": 30,
    "width": int,
    "height": int,
    "pause_key": pyray.KeyboardKey.KEY_P,
}

goto_scene = -1
debug = False
random = Random_names()
random.load_names()


class MenuScene:
    def activation(self, scene_changed: bool):
        if scene_changed:
            pass

    def process(self):
        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 -
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "New Game"
        ):
            set_scene(1)

        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2,
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Settings"
        ):
            set_scene(2)

        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 +
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Highscore Table"
        ):
            set_scene(3)

        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 + (
                Settings.menu_button_height * 2 + 10 * 2),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Exit"
        ):
            pyray.close_window()
            exit(0)

    def draw(self):
        if debug:
            draw_debug_info("MENU")


#  На игровую сцену была добавлена ПАУЗА
#  Я создал новую переменную, к ней можно обратиться командой Settings.game_pause_on (или обратившись в config.py)
#
#  Если пауза включена - game_pause_on = True
#  Иначе - game_pause_on = False
#
#  К движению NPC, игрока и тд, завязывайтек эту переменную как доп. условие, чтобы при паузе все зависли
def reset():
    Settings.pink_ghost.reset()
    Settings.blue_ghost.reset()
    Settings.red_ghost.reset()
    Settings.orange_ghost.reset()
    Settings.pacman.reset()
#  Settings.death_seeds_count = 0


class GameScene:
    def __init__(self):
        self.field_drawer = FieldDrawer(Settings.field, Settings.cell_size)
        self.score = ScoreDrawer(700, 0, "Score is {}", 25, colors.WHITE)
        self.life_drawer = LifeDrawer()
        self.start_time = None

    def activation(self, scene_changed: bool):
        if scene_changed:
            Settings.pacman.score.reset()
            pause("ACTIVATION")
            overlay_end_scene("ACTIVATION")
            Settings.sounds.pause_sounds()
            pyray.play_sound(Settings.sounds.game_start)
            Settings.game_stop = False
            Settings.field.make_map()
            reset()
            Settings.death_seeds_count = 0
            self.start_time = time.time()
            self.field_drawer.make_cells_list()

    def process(self):
        pause("PROCESS")
        if not Settings.game_stop and time.time() - self.start_time >= 2:
            Settings.pacman.logic(
                Settings.field.field, Settings.cell_size, self.field_drawer.cells,
                [Settings.red_ghost, Settings.pink_ghost,
                    Settings.blue_ghost, Settings.orange_ghost],
                Settings.life_counter,
                self
            )
            Settings.red_ghost.logic(
                Settings.field.field, Settings.cell_size, Settings.pacman)
            Settings.pink_ghost.logic(
                Settings.field.field, Settings.cell_size, Settings.pacman)
            Settings.blue_ghost.logic(
                Settings.field.field, Settings.cell_size, Settings.pacman)
            Settings.orange_ghost.logic(
                Settings.field.field, Settings.cell_size, Settings.pacman)

    def draw(self):
        self.field_drawer.draw()
        self.life_drawer.draw_lives(Settings.life_counter.lives)
        self.score.recreate_text(int(Settings.score_counter.show()))
        self.score.recreate_text(int(Settings.pacman.score.show()))
        self.score.draw()
        Settings.pacman.draw()
        Settings.red_ghost.draw(Settings.pacman)
        Settings.pink_ghost.draw(Settings.pacman)
        Settings.blue_ghost.draw(Settings.pacman)
        Settings.orange_ghost.draw(Settings.pacman)
        ready_sign("READY?", 17)
        if time.time() - self.start_time >= 2:
            Settings.pacman.draw()
            Settings.red_ghost.draw(Settings.pacman)
            Settings.pink_ghost.draw(Settings.pacman)
            Settings.blue_ghost.draw(Settings.pacman)
            Settings.orange_ghost.draw(Settings.pacman)
        pause("DRAW")
        overlay_end_scene("DRAW")

        if debug and not Settings.game_pause_on:
            draw_debug_info("GAME - PLAY")
        elif debug and Settings.game_pause_on:
            draw_debug_info("GAME - PAUSE")


class SettingsScene:
    def __init__(self):
        self.turn = TurnCondition(Settings.sounds_on)

    def activation(self, scene_changed: bool):
        if scene_changed:
            return

    def process(self):
        global random
        pyray.draw_text("Your name is {}".format(Settings.user_name),
                        Settings.width // 2 - 250, 100, 50, colors.WHITE)
        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2,
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Randomize nick"
        ):
            Settings.user_name = random.randomizer()
        if pyray.gui_button(
            pyray.Rectangle(
                20,
                Settings.height - Settings.menu_button_height - 20,
                Settings.menu_button_width,
                Settings.menu_button_height
            ),
            "Back to Menu"
        ):
            set_scene(0)
        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 +
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
                # <- bool + recalculable text
            ), "Sound turn {}".format(TurnCondition(Settings.sounds_on).show())
        ):
            Settings.sounds_on = not Settings.sounds_on

    def draw(self):
        if debug:
            draw_debug_info("SETTINGS")


class HighScoreScene:
    def __init__(self):
        self.highscoreDrawer = HighscoreTableDrawer(
            Settings.highscoreTable.scores)

    def activation(self, scene_changed: bool):
        if scene_changed:
            Settings.highscoreTable.load_scores()
            self.highscoreDrawer = HighscoreTableDrawer(
                Settings.highscoreTable.scores)

    def process(self):
        if pyray.gui_button(
            pyray.Rectangle(
                20,
                Settings.height - Settings.menu_button_height - 20,
                Settings.menu_button_width,
                Settings.menu_button_height
            ),
            "Back to Menu"
        ):
            set_scene(0)

    def draw(self):
        if debug:
            draw_debug_info("HIGHSCORE")
        self.highscoreDrawer.draw_table(Settings.width, Settings.height)


def pause(mode: str):
    if mode == "ACTIVATION":
        Settings.game_pause_on = False

        pause_memory["x"] = pause_memory["spaceX"]
        pause_memory["y"] = pause_memory["spaceY"]

        pause_memory["width"] = Settings.width - pause_memory["spaceX"] * 2
        pause_memory["height"] = Settings.height - pause_memory["spaceY"] * 2

    elif mode == "PROCESS":
        if Settings.game_pause_on:
            Settings.sounds.pause_sounds()
        else:
            Settings.sounds.resume_sounds()

        if pyray.is_key_pressed(pause_memory["pause_key"]):
            Settings.game_pause_on = not Settings.game_pause_on
            Settings.game_stop = not Settings.game_stop
    elif mode == "DRAW" and Settings.game_pause_on:
        pyray.draw_rectangle_rounded(
            pyray.Rectangle(
                pause_memory["x"],
                pause_memory["y"],
                pause_memory["width"],
                pause_memory["height"]
            ), 0.1, 5, [45, 45, 45, 153]
        )

        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 -
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Continue"
        ):
            Settings.game_pause_on = False
            Settings.game_stop = False

        elif pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2,
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Replay"
        ):
            set_scene(1)

        elif pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 +
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Back to Menu"
        ):
            set_scene(0)


def overlay_end_scene(scene_type: str):
    if scene_type == "DRAW" and Settings.game_over:
        Settings.game_stop = True
        Settings.life_counter.lives = 3
        text = "Game Over"
        game_over_title = RecalculableText(
            Settings.width // 2 -
            pyray.measure_text(text, 50) // 2, 200, text, 50,
            colors.PINK
        )
        pyray.draw_rectangle(0, 0, Settings.width,
                             Settings.height, [111, 111, 111, 200])
        game_over_title.draw()
        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 +
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Back to Menu"
        ):
            set_scene(0)
            Settings.highscoreTable.add_score(
                Settings.user_name, Settings.pacman.score.counter)
            Settings.highscoreTable.save_scores()
    if scene_type == "DRAW" and Settings.game_finished:
        Settings.game_stop = True
        Settings.life_counter.lives = 3
        text = "YOU WON OMG"
        game_over_title = RecalculableText(
            Settings.width // 2 -
            pyray.measure_text(text, 50) // 2, 200, text, 50,
            colors.PINK
        )
        pyray.draw_rectangle(0, 0, Settings.width,
                             Settings.height, [111, 111, 111, 200])
        game_over_title.draw()
        if pyray.gui_button(
            pyray.Rectangle(
                Settings.width // 2 - Settings.menu_button_width // 2,
                Settings.height // 2 - Settings.menu_button_height // 2 +
                (Settings.menu_button_height + 10),
                Settings.menu_button_width,
                Settings.menu_button_height
            ), "Back to Menu"
        ):
            set_scene(0)
            Settings.highscoreTable.add_score(
                Settings.user_name, Settings.pacman.score.counter)
            Settings.highscoreTable.save_scores()
    elif scene_type == "ACTIVATION":
        Settings.game_over = False
        Settings.game_finished = False


def draw_debug_info(name_scene: str):
    pyray.draw_text("SCENE: " + name_scene, 10, 10, 14, colors.DARKGRAY)


def set_debug(is_debug):
    global debug
    debug = is_debug


def set_scene(index):
    global goto_scene
    goto_scene = index


def check_scene(scene_index: int):
    global goto_scene
    if goto_scene == -1:
        if debug:
            print(debug)
            scene_list = [
                pyray.KeyboardKey.KEY_ZERO,
                pyray.KeyboardKey.KEY_ONE,
                pyray.KeyboardKey.KEY_TWO,
                pyray.KeyboardKey.KEY_THREE
            ]

            key = pyray.get_key_pressed()
            for i in range(len(scene_list)):
                if key == scene_list[i]:
                    return i, True
            else:
                return scene_index, False
        else:
            return scene_index, False
    else:
        temp = goto_scene
        goto_scene = -1
        return temp, True


def ready_sign(text, size):
    if pyray.is_sound_playing(Settings.sounds.game_start):
        pyray.draw_text(
            text,
            Settings.width // 2 - pyray.measure_text(
                text,
                size
            ) // 2,
            Settings.height // 2 - 100,
            size,
            colors.ORANGE
        )

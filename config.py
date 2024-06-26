from logic.highscore import HighscoreTable
from logic.field import Field
from objects.ghosts import Ghost
from objects.sounds import Sounds
from logic.life import LifeCounter
from logic.score import ScoreCounter
from objects.images.pacman import Pacman


class Settings:
    death_seeds_count = 0
    highscoreTable: HighscoreTable = HighscoreTable()
    sounds: Sounds = Sounds()
    life_counter: LifeCounter = LifeCounter()
    score_counter: ScoreCounter = ScoreCounter()
    field: Field = Field()
    scene_index: int = 0
    scene_changed: bool = True
    width: int = 1000
    height: int = 520
    debug_mode: bool = False
    game_pause_on: bool = False
    game_over: bool = False
    game_finished: bool = False
    sounds_on: bool = True
    menu_button_width: int = 90
    menu_button_height: int = 60
    cell_size: int = 20
    user_name: str = "User_1"
    pacman: Pacman = Pacman(380, 480, "none", sounds)
    red_ghost: Ghost = Ghost(500, 260, "red", "left")
    pink_ghost: Ghost = Ghost(500, 240, "pink", "left")
    blue_ghost: Ghost = Ghost(520, 260, "blue", "left")
    orange_ghost: Ghost = Ghost(520, 240, "orange", "left")

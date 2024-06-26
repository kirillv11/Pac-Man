import pyray


class TurnCondition:
    def __init__(self, cond: bool):
        self.condition = cond

    def show(self):
        if self.condition:
            return "On"
        return "Off"


class Sounds:
    def __init__(self):
        pyray.init_audio_device()

        self.death = pyray.load_sound("resources/sounds/death.wav")
        self.eat = pyray.load_sound("resources/sounds/eat.wav")
        self.eat_fruit = pyray.load_sound("resources/sounds/eat_fruit.wav")
        self.eat_ghost = pyray.load_sound("resources/sounds/eat_ghost.wav")
        self.extend = pyray.load_sound("resources/sounds/extend.wav")
        self.game_start = pyray.load_sound("resources/sounds/game_start.wav")
        self.intermission = pyray.load_sound(
            "resources/sounds/intermission.wav")
        self.power_pellet = pyray.load_sound(
            "resources/sounds/power_pellet.wav")
        self.retreating = pyray.load_sound("resources/sounds/retreating.wav")
        self.siren = pyray.load_sound("resources/sounds/siren.wav")

    def pause_sounds(self):
        pyray.pause_sound(self.death)
        pyray.pause_sound(self.eat)
        pyray.pause_sound(self.eat_fruit)
        pyray.pause_sound(self.eat_ghost)
        pyray.pause_sound(self.extend)
        pyray.pause_sound(self.game_start)
        pyray.pause_sound(self.intermission)
        pyray.pause_sound(self.power_pellet)
        pyray.pause_sound(self.retreating)
        pyray.pause_sound(self.siren)

    def resume_sounds(self):
        pyray.resume_sound(self.death)
        pyray.resume_sound(self.eat)
        pyray.resume_sound(self.eat_fruit)
        pyray.resume_sound(self.eat_ghost)
        pyray.resume_sound(self.extend)
        pyray.resume_sound(self.game_start)
        pyray.resume_sound(self.intermission)
        pyray.resume_sound(self.power_pellet)
        pyray.resume_sound(self.retreating)
        pyray.resume_sound(self.siren)

    @staticmethod
    def check_sound(is_sounds_on):
        if is_sounds_on:
            pyray.set_master_volume(0.5)
        else:
            pyray.set_master_volume(0)

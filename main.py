import pyray
from raylib import colors
from scenes.etc import MenuScene, GameScene, SettingsScene, HighScoreScene, check_scene, set_debug
from config import Settings
from sys import exit


def main():
    pyray.init_window(Settings.width, Settings.height, "Pac-man")
    pyray.set_target_fps(60)

    #  Оглашение всех сцен
    menu = MenuScene()
    game = GameScene()
    settings = SettingsScene()
    highscore = HighScoreScene()
    set_debug(Settings.debug_mode)

    # Инициализация Pac-man и Ghost
    Settings.pacman.init_texture()
    Settings.red_ghost.init_image()
    Settings.blue_ghost.init_image()
    Settings.pink_ghost.init_image()
    Settings.orange_ghost.init_image()

    # инициализация звуков
    # main_sound = Settings.sounds.intermission
    # other_sound = Settings.sounds.game_start

    # цикл игры
    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(colors.BLACK)

        if Settings.scene_changed:
            pyray.stop_sound(Settings.sounds.game_start)
            pyray.stop_sound(Settings.sounds.intermission)

        if Settings.scene_index == 0:  # 0 - menu
            if not pyray.is_sound_playing(Settings.sounds.intermission):
                pyray.play_sound(Settings.sounds.intermission)
            menu.activation(Settings.scene_changed)
            menu.process()
            menu.draw()
        elif Settings.scene_index == 1:  # 1 - game
            game.activation(Settings.scene_changed)
            game.process()
            game.draw()
        elif Settings.scene_index == 2:  # 2 - settings
            if not pyray.is_sound_playing(Settings.sounds.game_start):
                pyray.play_sound(Settings.sounds.game_start)
            settings.activation(Settings.scene_changed)
            settings.process()
            settings.draw()
        elif Settings.scene_index == 3:  # 3 - table of records
            if not pyray.is_sound_playing(Settings.sounds.game_start):
                pyray.play_sound(Settings.sounds.game_start)
            highscore.activation(Settings.scene_changed)
            highscore.process()
            highscore.draw()
        Settings.scene_index, Settings.scene_changed = check_scene(
            Settings.scene_index)
        Settings.sounds.check_sound(Settings.sounds_on)
        pyray.end_drawing()

    pyray.close_window()
    exit(0)


if __name__ == '__main__':
    main()

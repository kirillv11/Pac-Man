import pyray
from raylib import colors


class HighscoreTableDrawer:
    def __init__(self, highscores):
        self.highscores = highscores

    def draw_table(self, width, height):
        text = "Highscore Table"
        pyray.draw_text(text, width // 2 -
                        pyray.measure_text(text, 30) // 2, 20, 30, colors.WHITE)
        for i, player in enumerate(self.highscores, start=1):
            text_score = f"{i}. {player[0]} - {player[1]}"
            pyray.draw_text(
                text_score, width // 2 -
                pyray.measure_text(text_score, 20) // 2, (50 +
                                                          (25 * i)), 20, colors.WHITE
            )

import pyray


class Text:
    def __init__(self, x: int, y: int, text: str, size: int, color: pyray.Color):
        self.rect = [x, y]
        self.text = text
        self.size = size
        self.color = color

    def draw(self):
        pyray.draw_text(
            self.text, self.rect[0], self.rect[1], self.size, self.color)


class RecalculableText(Text):
    def __init__(self, x: int, y: int, text: str, size: int, color: pyray.Color):
        super().__init__(x, y, text, size, color)
        self.text_format = self.text

    def recreate_text(self, *args, **kwargs):
        self.text = self.text_format.format(*args, **kwargs)


class ScoreDrawer(RecalculableText):
    def __init__(self, x: int, y: int, text: str, size: int, color: pyray.Color, n=0):
        super().__init__(x, y, text, size, color)
        self.count = n

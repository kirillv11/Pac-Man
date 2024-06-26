class ScoreCounter:
    def __init__(self):
        self.counter = 0

    def add(self, x: int):
        self.counter += x

    def show(self):
        return self.counter

    def reset(self):
        self.counter = 0

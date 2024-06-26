class Field:
    def __init__(self):
        self.field = list()

    def make_map(self):
        self.field.clear()
        f = open("resources/field.txt", "r")
        for line in f:
            self.field.append(line.split())

import random


class Random_names:
    def __init__(self):
        self.list = []

    def load_names(self):
        with open('resources/random_names.txt', 'r', encoding="utf-8") as name_list:
            for line in name_list:
                name = line.strip()
                self.list.append(name)

    def randomizer(self):
        return self.list[random.randint(0, len(self.list)-1)]

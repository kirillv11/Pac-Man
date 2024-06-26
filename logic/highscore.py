class HighscoreTable:
    def __init__(self):
        self.scores = list()

    def load_scores(self):
        self.scores.clear()
        with open('resources/highscores.txt', 'r', encoding="utf-8") as scores_list:
            for line in scores_list:
                player_name, player_score = line.strip().split(" - ")
                self.add_score(player_name, int(player_score))

    def save_scores(self):
        with open('resources/highscores.txt', 'w', encoding="utf-8") as scores_list:
            for player_name, player_score in self.scores:
                scores_list.write(f"{player_name} - {player_score}\n")
            scores_list.close()

    def add_score(self, player_name, player_score):
        if len(self.scores) < 10 or player_score > self.scores[-1][1]:
            self.scores.append([player_name, player_score])
            self.scores.sort(key=lambda x: x[1], reverse=True)
            self.scores = self.scores[:10]

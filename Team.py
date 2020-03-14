class Team( object ):

    def __init__(self, game, color, goal, pitch_half):
        self.game = game
        self.color = color
        self.goal = goal
        self.pitch_half = pitch_half
        self.players = []
        self.score = 0

    def add_player(self, player):
        self.players.append(player)
        player.color = self.color

    def remove_player(self, player):
        self.players.remove(player)

    def reset_score(self):
        self.score = 0

    def add_point(self):
        self.score += 1

    def size(self):
        return len(self.players)

    def reset_positions(self):
        i = 1
        for obj in self.players:
            pos_x = obj.game.screen_w / 2 + self.pitch_half * obj.game.pitch_w / 4
            pos_y = (obj.game.screen_h - obj.game.pitch_h) / 2 + i * obj.game.pitch_h / 4
            obj.set_move((0,0), (pos_x, pos_y))
            i += 1

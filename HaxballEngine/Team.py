from HaxballEngine.Properties import InternalProperties


class Team(object):

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
        for player in self.players:
            pos_x = InternalProperties.SCREEN_WIDTH / 2 + self.pitch_half * InternalProperties.PITCH_WIDTH / 4
            pos_y = (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2 + i * InternalProperties.PITCH_HEIGHT / 4
            player.set_move((0, 0), (pos_x, pos_y))
            i += 1

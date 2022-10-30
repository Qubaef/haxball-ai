from HaxballEngine.CirclePhysical import CirclePhysical


class Post(CirclePhysical):
    def __init__(self, game, px, py):
        super().__init__(game, px, py, 0, 1, 6, (0, 0, 0))
        self.to_sector_add()

    def update(self):
        return 1

    def set_p(self, px, py):
        return 1

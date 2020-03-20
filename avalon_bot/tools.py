class GameInfo:

    def __init__(self, state, creator, players, cur_king=None, cur_lady=None):
        self.state = state
        self.creator = creator
        self.players = players
        self.cur_king = cur_king
        self.cur_lady = cur_lady
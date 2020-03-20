class GameInfo:

    additional_roles = {
            'Morgana': False,
            'Mordred': False,
            'Oberon': False
        }

    def __init__(self, state, creator, players, cur_king=None, cur_lady=None):
        self.state = state
        self.creator = creator
        self.players = players
        self.cur_king = cur_king
        self.cur_lady = cur_lady
        self.successful_exp = 0
        self.failed_exp = 0
        self.exp_size = []
        self.players_nick_to_id = dict()
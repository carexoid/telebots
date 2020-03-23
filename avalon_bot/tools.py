class GameInfo:

    additional_roles = {
            'Morgana': False,
            'Mordred': False,
            'Oberon': False
        }

    lady_lake = False

    expedition_size = {5:  [2, 3, 2, 3, 3],
                       6:  [2, 3, 4, 3, 4],
                       7:  [2, 3, 3, 4, 4],
                       8:  [3, 4, 4, 5, 5],
                       9:  [3, 4, 4, 5, 5],
                       10: [3, 4, 4, 5, 5]}

    def __init__(self, state, creator, players, cur_king=None, cur_lady=None):
        self.state = state
        self.creator = creator
        self.players = players
        self.cur_king = cur_king
        self.cur_lady = cur_lady
        self.successful_exp = 0
        self.failed_exp = 0
        self.exp_size = [0, 0, 0, 0, 0]
        self.players_nick_to_id = dict()
        self.cur_voting_for_exp = dict.copy(players)
        self.cur_exp = []
        self.people_in_exp = dict()
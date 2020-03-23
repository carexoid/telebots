class GameInfo:
    expedition_size = {5: [2, 3, 2, 3, 3],
                       6: [2, 3, 4, 3, 4],
                       7: [2, 3, 3, 4, 4],
                       8: [3, 4, 4, 5, 5],
                       9: [3, 4, 4, 5, 5],
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
        self.additional_roles = {
            'Morgana': False,
            'Mordred': False,
            'Oberon': False
        }
        self.lady_lake = False
        self.order = []
        self.checked = []

    def change_roles(self, role):
        if self.additional_roles[role]:
            self.additional_roles[role] = False
            return " has removed"
        else:
            self.additional_roles[role] = True
            return " has added"

    def change_lady(self):
        if self.lady_lake:
            self.lady_lake = False
            return " has removed"
        else:
            self.lady_lake = True
            return " has added"

    def king_rotation(self):
        self.cur_king = (self.cur_king + 1) % len(self.order)

    def get_num_of_exp(self):
        return self.successful_exp + self.failed_exp
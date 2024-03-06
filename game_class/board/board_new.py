from .board_parent import BoardParent


class BoardNew(BoardParent):
    def __init__(self, board_size: int):
        super().__init__(board_size)
        self.player_1_score = 0
        self.player_2_score = 0

    def addNode(self, x: int, y: int, player: int):
        player_1_local_score = self.get_value(x, y, 1)
        player_2_local_score = self.get_value(x, y, -1)

        super().addNode(x, y, player)

        player_1_changed_score = self.get_value(x, y, 1) - player_1_local_score
        player_2_changed_score = self.get_value(x, y, -1) - player_2_local_score

        self.player_1_score += player_1_changed_score
        self.player_2_score += player_2_changed_score

    def reset(self):
        super().reset()
        self.player_1_score = 0
        self.player_2_score = 0

    def get_value(self, x: int, y: int, player: int) -> float:
        """
        Return the value of the node.
        :param x:
        :param y:
        :param player:
        :return: q_value for this specific node(move)
        """
        plist = [
            '____X',
            '___X_',
            '___XX',
            '__X__',
            '__X_X',
            '__XX_',
            '__XXX',
            '_X___',
            '_X__X',
            '_X_X_',
            '_X_XX',
            '_XX__',
            '_XX_X',
            '_XXX_',
            '_XXXX',
            'X____',
            'X___X',
            'X__X_',
            'X__XX',
            'X_X__',
            'X_X_X',
            'X_XX_',
            'X_XXX',
            'XX___',
            'XX__X',
            'XX_X_',
            'XX_XX',
            'XXX__',
            'XXX_X',
            'XXXX_',
            'XXXXX',
        ]

        patterns_X = {
            k: [0, 1, 6, 33, 200, 1575][k.count('X')] for k in plist
        }

        player_score = 0
        opponent_score = 0
        window_size = 5
        opponent = -player

        for line in self.lines(x, y):
            if len(line) < window_size:
                continue
            for i in range(len(line) - window_size + 1):
                window = line[i:i + window_size]
                window_str = self.state_to_string(window, player)
                if window_str is None:
                    continue
                if window_str in patterns_X:
                    player_score += patterns_X[window_str]
                window_str = self.state_to_string(window, opponent)
                if window_str in patterns_X:
                    opponent_score += patterns_X[window_str]

        return player_score - opponent_score

    @staticmethod
    def state_to_string(sub_state, target_player):
        """
        Convert a sub state to a string.
        :param sub_state: the sub state
        :param target_player: the player who adds this stone
        :return: string representation of the sub state
        """
        contains_target = False
        contains_opponent = False

        for cell in sub_state:
            if cell and cell.player == target_player:
                contains_target = True
            elif cell and cell.player == -target_player:
                contains_opponent = True
        if contains_target and contains_opponent:
            return None

        return ''.join('X' if (cell and cell.player == target_player) else '_' for cell in sub_state)

    def lines(self, x, y):
        """
        four directions of the piece coordinate
        :param x:
        :param y:
        :return:
        """
        yield [self.board[x][i] for i in range(self.board_size)]
        yield [self.board[i][y] for i in range(self.board_size)]

        start_dx = min(x, y)
        end_dx = min(self.board_size - 1 - x, self.board_size - 1 - y)
        yield [self.board[x - start_dx + i][y - start_dx + i] for i in range(start_dx + end_dx + 1)]

        start_dx = min(x, self.board_size - 1 - y)
        end_dx = min(self.board_size - 1 - x, y)
        yield [self.board[x - start_dx + i][y + start_dx - i] for i in range(start_dx + end_dx + 1)]

    def get_score(self, player: int):
        """
        Return the score of the player.
        :param player:  the player
        :return: the board score of the player
        """
        if player == 1:
            return self.player_1_score
        else:
            return self.player_2_score




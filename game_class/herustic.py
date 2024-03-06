from .value_functions import BaseValueFunctionSingle
import numpy as np


class HeuristicValueFunctionsSizeN(BaseValueFunctionSingle):
    def __init__(self, size):
        """
        初始化的时候要把offset_lower, offset_upper, size传进来
        适配不同尺寸棋盘的value_function
        :param size: 棋盘大小
        """
        super().__init__()
        self.size = size

    def get_V(self, state: tuple[int, ...], player: int, action_space: set[int]) -> float:
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

        for line in self.lines(state):
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
        contains_target = False
        contains_opponent = False

        for cell in sub_state:
            if cell == target_player:
                contains_target = True
            elif cell == -target_player:
                contains_opponent = True
        if contains_target and contains_opponent:
            return None

        return ''.join('X' if cell == target_player else '_' for cell in sub_state)

    def lines(self, state: tuple[int, ...]):
        board = np.array(state).reshape(self.size, self.size)
        for i in range(self.size):
            yield board[i, :]
            yield board[:, i]

        for d in range(-(self.size - 5), self.size - 4):
            yield np.diagonal(board, offset=d)
            yield np.diagonal(np.fliplr(board), offset=d)
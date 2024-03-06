import copy

from .value_functions.base_value_function import BaseValueFunction
from .TicTacToeSizeN import TicTacToeSizeN
from .policies.q_policies.base_q_policy import BaseQPolicySingle
from typing import Optional


class MinMaxPolicySizeN(BaseQPolicySingle):
    """
    MinMaxPolicySizeN fit for 五子棋 size larger than 6
    初始化的时候要把game_cls传进来， game_cls是一个类，用来初始化一个game对象
    size是多少，请选择size多少的heuristic
    """
    def __init__(self,
                 game_cls,
                 board_class,
                 heuristic: Optional[BaseValueFunction] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_cls = game_cls
        self.heuristic = heuristic
        self.board_class = board_class

    def min_max(self, game: TicTacToeSizeN, is_max_player, cloned_game_player, depth, alpha=-float('inf'), beta=float('inf')):
        # if game.is_terminated():
        #     return self.heuristic.get_V(game.get_state(), cloned_game_player, game.get_actions())
        #
        # if depth == 0:
        #     return self.heuristic.get_V(game.get_state(), cloned_game_player, game.get_actions())
        if game.is_terminated() or depth == 0:
            if self.heuristic:
                return self.heuristic.get_V(game.get_state(), cloned_game_player, game.get_actions())
            else:
                return game.second_layer_board.get_score(cloned_game_player)

        if is_max_player:
            best_score = -float('inf')
            for action in game.get_actions():
                cloned_game = copy.deepcopy(game)
                cloned_game.move(action)
                score = self.min_max(cloned_game, False, cloned_game_player, depth - 1, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if best_score >= beta:
                    break
            return best_score
        else:
            best_score = float('inf')
            for action in game.get_actions():
                cloned_game = copy.deepcopy(game)
                cloned_game.move(action)
                score = self.min_max(cloned_game, True, cloned_game_player, depth - 1, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if best_score <= alpha:
                    break
            return best_score

    def get_all_Qs(self, state: tuple[int, ...], player: int, action_space: set[int]) -> dict[int, float]:
        q_values = {}
        # depth = (int(len(state) - len(action_space)) // int(len(state)**0.5)) // 2 * 2 + 1
        depth = 1
        for action in action_space:
            new_game = self.game_cls.from_state(board_class=self.board_class, state=state, player=player)
            cloned_game_player = new_game.clone().player
            new_game.move(action)
            score = self.min_max(new_game, False, cloned_game_player, depth=depth)
            q_values[action] = score
        return q_values

    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> None:
        raise NotImplementedError
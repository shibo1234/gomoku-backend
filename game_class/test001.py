from game_class.minimax_policy import MinMaxPolicySizeN
from game_class.TicTacToeSizeN import TicTacToeSizeN
from game_class.herustic import HeuristicValueFunctionsSizeN
import numpy as np
from game_class.board.board_correct import BoardCorrect
from game_class.board.board_new import BoardNew


if __name__ == '__main__':
    ttt = TicTacToeSizeN(BoardCorrect, size=15)
    ttt_1 = TicTacToeSizeN(BoardNew, size=15)
    heuristic = HeuristicValueFunctionsSizeN(15)
    min_max_policy = MinMaxPolicySizeN(ttt, BoardCorrect, heuristic)
    min_max_policy_1 = MinMaxPolicySizeN(ttt_1, BoardNew)

    ttt.move(25)
    ttt_1.move(25)
    correct_move = min_max_policy(ttt.get_state(), ttt.player, ttt.get_actions())
    new_move = min_max_policy_1(ttt_1.get_state(), ttt_1.player, ttt_1.get_actions())
    print(correct_move)
    print(min_max_policy.get_all_Qs(ttt.get_state(), ttt.player, ttt.get_actions()))
    print(new_move)
    print(min_max_policy_1.get_all_Qs(ttt_1.get_state(), ttt_1.player, ttt_1.get_actions()))
    # assert correct_move == new_move

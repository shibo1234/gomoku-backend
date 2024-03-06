import copy
from typing import Callable, Optional, Type
from .board.board_parent import BoardParent
import numpy as np


class TicTacToeSizeN:
    """
    Game class fit for any size larger than 6
    default size 6, adjust when instantiate this class
    state_formatter: function to format state
    """
    def __init__(self,
                 board_class: Type[BoardParent],
                 start_player: int = 1,
                 default_state_formatter: Callable[[tuple[int, ...]], str] = str,
                 size=6):
        self.size = size
        self.board = np.zeros(size * size, dtype=int)
        self.player = start_player
        self.default_state_formatter = default_state_formatter
        self.action_history = []
        self.second_layer_board = board_class(size)

    @classmethod
    def from_state(cls, board_class, state: tuple[int, ...], player: int):
        obj = TicTacToeSizeN(board_class=board_class, size=int(len(state) ** 0.5))
        # obj = cls(board_class=board_class, size=int(len(state) ** 0.5))
        obj.update_state(state, player)
        return obj

    @staticmethod
    def player_formatter(player: int) -> str:
        symbol_mapping = {0: " ", 1: "X", -1: "O"}
        return symbol_mapping[player]

    def state_formatter(self) -> str:
        size = self.size
        formatted_state = "\n"
        for i in range(size):
            formatted_state += "+" + "---+" * size + "\n"
            row = self.board[i*size:(i+1)*size]
            formatted_state += "| " + " | ".join(TicTacToeSizeN.player_formatter(cell) for cell in row) + " |\n"
        formatted_state += "+" + "---+" * size + "\n"
        return formatted_state

    def __str__(self):
        format_str = '\n+---+---+---+\n|{:^size}|{:^size}|{:^size}|' * self.size + '\n+---+---+---+\n'
        return format_str.format(*np.array([' ', 'X', 'O'])[self.board].tolist())

    # TODO: use __str__
    def render(self, state_formatter: Optional[Callable[[tuple[int, ...]], str]] = None):
        print(self.state_formatter(), flush=True)

    def update_state(self, state: tuple[int, ...], player: int):
        # self.board = np.array(state, dtype=int)
        # self.player = player
        # for idx, value in enumerate(state):
        #     if value != 0:
        #         x, y = divmod(idx, self.size)
        #         self.second_layer_board.addNode(x, y, value)

        player_mapping = {'black': 1, 'white': -1, None: 0}
        cleaned_state = [player_mapping[cell] if cell in player_mapping else cell for cell in state]
        self.board = np.array(cleaned_state, dtype=int)
        self.player = player
        for idx, value in enumerate(cleaned_state):
            if value != 0:
                x, y = divmod(idx, self.size)
                self.second_layer_board.addNode(x, y, value)

    def get_state(self) -> tuple[int, ...]:
        return tuple(self.board.astype(int).tolist())

    def get_actions(self):
        return set(np.where(self.board == 0)[0].tolist())

    def get_winner(self) -> int:
        """
        Check if there is a winner, traverse through all possible lines
        :return: player 1 or -1, tie or no winner 0
        """
        return self.second_layer_board.get_winner()

    def get_player(self):
        return self.player

    def get_last_player(self):
        return -self.player

    def is_terminated(self):
        return not self.get_actions() or self.get_winner() != 0

    def clone(self):
        return copy.deepcopy(self)

    def move(self, action):
        if self.board[action] != 0:
            raise Exception("Invalid move")
        x, y = divmod(action, self.size)
        self.board[action] = self.player
        self.second_layer_board.addNode(x, y, self.player)
        self.player = -self.player
        self.action_history.append(action)

    def agent_move(self, policy):
        state = self.get_state()
        actions = self.get_actions()
        best_action = policy(state, self.player, actions)
        self.move(best_action)
        x, y = divmod(best_action, self.size)
        return best_action

    def reset(self, start_player=1):
        self.second_layer_board.reset()
        self.board *= 0
        self.player = start_player

    def spawn(self, action):
        clone = self.clone()
        clone.move(action)
        return clone

    # TODO: value function
    def utility(self, player):
        if self.is_terminated():
            if self.get_winner() == 0:
                return 0
            return 10 if self.get_winner() == player else -10
        return 0

    def last_player(self):
        return -self.player

    def apply_action(self, action):
        if self.board[action] != 0:
            raise Exception("Invalid move")
        self.board[action] = self.player
        self.player = -self.player
        self.action_history.append(action)

    def undo_action(self):
        if not self.action_history:
            raise Exception("No actions to undo")
        last_action = self.action_history.pop()
        self.board[last_action] = 0
        self.player = -self.player

from ..base_policy import BasePolicy

from abc import abstractmethod
import random
import itertools as it
import numpy as np


class BaseQPolicy(BasePolicy):

    def __init__(self, stochastic: bool = False, temperature: float = 1.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stochastic = stochastic
        self.temperature = temperature

    def __call__(self, state: tuple[int, ...], player: int, action_space: set[int]) -> int:
        q_dict = self.get_all_Qs(state, player, action_space)
        if self.stochastic:
            probs = self._softmax(list(q_dict.values()), self.temperature)
            return random.choices(list(q_dict.keys()), weights=probs)[0]
        else:
            return max(q_dict, key=q_dict.__getitem__)

    def _softmax(self, x, temperature):
        x = np.array(x)
        e_x = np.exp((x - np.max(x)) / temperature)
        return (e_x / e_x.sum(axis=0)).tolist()

    def get_Q(self, state: tuple[int, ...], player: int, action: int) -> float:
        return self.get_all_Qs(state, player, {action})[action]

    def batch_get_Q(self, states: list[tuple[int, ...]], players: list[int], actions: list[int]) -> list[float]:
        return list(map(
            lambda qd: list(qd.values)[0],
            self.batch_get_all_Qs(states, players, [{action} for action in actions])
        ))

    @abstractmethod
    def get_all_Qs(self, state: tuple[int, ...], player: int, action_space: set[int]) -> dict[int, float]:
        return self.batch_get_all_Qs([state], [player], [action_space])[0]

    @abstractmethod
    def batch_get_all_Qs(self,
                         states: list[tuple[int, ...]],
                         players: list[int],
                         action_spaces: list[set[int]]) -> list[dict[int, float]]:
        return list(it.starmap(self.get_all_Qs, zip(states, players, action_spaces)))

    @abstractmethod
    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> float:
        return self.batch_update_Q([state], [player], [action], [Q])

    @abstractmethod
    def batch_update_Q(self,
                       states: list[tuple[int, ...]],
                       players: list[int],
                       actions: list[int],
                       Qs: list[float]) -> float:
        return np.mean(list(it.starmap(self.update_Q, zip(states, players, actions, Qs))))


class BaseQPolicySingle(BaseQPolicy):

    @abstractmethod
    def get_all_Qs(self,
                   state: tuple[int, ...],
                   player: int,
                   action_space: set[int]) -> dict[int, float]:
        raise NotImplementedError

    def batch_get_all_Qs(self,
                         states: list[tuple[int, ...]],
                         players: list[int],
                         action_spaces: list[set[int]]) -> list[dict[int, float]]:
        return super().batch_get_all_Qs(states, players, action_spaces)

    @abstractmethod
    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> float:
        raise NotImplementedError

    def batch_update_Q(self,
                       states: list[tuple[int, ...]],
                       players: list[int],
                       actions: list[int],
                       Qs: list[float]) -> float:
        return super().batch_update_Q(states, players, actions, Qs)


class BaseQPolicyBatch(BaseQPolicy):

    def get_all_Qs(self, state: tuple[int, ...], player: int, action_space: set[int]) -> dict[int, float]:
        return super().get_all_Qs(state, player, action_space)

    @abstractmethod
    def batch_get_all_Qs(self,
                         states: list[tuple[int, ...]],
                         players: list[int],
                         action_spaces: list[set[int]]) -> list[dict[int, float]]:
        raise NotImplementedError

    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> float:
        return super().update_Q(state, player, action, Q)

    @abstractmethod
    def batch_update_Q(self,
                       states: list[tuple[int, ...]],
                       players: list[int],
                       actions: list[int],
                       Qs: list[float]) -> float:
        raise NotImplementedError

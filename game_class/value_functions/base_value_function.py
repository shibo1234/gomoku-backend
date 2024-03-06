from abc import ABC, abstractmethod


class BaseValueFunction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_V(self, state: tuple[int, ...], player: int, action_space: set[int]) -> float:
        return self.batch_get_V([state], [player])[0]

    @abstractmethod
    def batch_get_V(self,
                    states: list[tuple[int, ...]],
                    players: list[int],
                    action_spaces: list[set[int]]) -> list[float]:
        return [self.get_V(state, player) for state, player in zip(states, players)]


class BaseValueFunctionSingle(BaseValueFunction):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_V(self, state: tuple[int, ...], player: int, action_space: set[int]) -> float:
        raise NotImplementedError

    def batch_get_V(self,
                    states: list[tuple[int, ...]],
                    players: list[int],
                    action_spaces: list[set[int]]) -> list[float]:
        return super().batch_get_V(states, players)


class BaseValueFunctionBatch(BaseValueFunction):
    def __init__(self):
        super().__init__()

    def get_V(self, state: tuple[int, ...], player: int, action_space: set[int]) -> float:
        return super().get_V(state, player)

    @abstractmethod
    def batch_get_V(self,
                    states: list[tuple[int, ...]],
                    players: list[int],
                    action_spaces: list[set[int]]) -> list[float]:
        raise NotImplementedError


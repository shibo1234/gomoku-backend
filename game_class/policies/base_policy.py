from abc import ABC, abstractmethod
from typing import Optional


class BasePolicy(ABC):

    def __init__(self, name: Optional[str] = None):
        self._name = name or self.__class__.__name__

    @abstractmethod
    def __call__(self, state: tuple[int, ...], player: int, action_space: set[int]) -> int:
        raise NotImplementedError

    def get_name(self) -> str:
        return self._name

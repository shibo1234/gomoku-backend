from .base_policy import BasePolicy


class DummyPolicy(BasePolicy):
    def __call__(self, state: tuple[int, ...], player: int, actions: set[int]) -> int:
        raise NotImplementedError

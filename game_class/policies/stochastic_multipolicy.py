from .base_policy import BasePolicy
import random
from typing import Optional


class StochasticMultiPolicy(BasePolicy):
    def __init__(self, policies: list[BasePolicy], probs: Optional[list[float]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.policies = policies
        self.probs = probs or [1/len(policies) for _ in policies]

    def __call__(self, state: tuple[int, ...], player: int, actions: set[int]) -> int:
        return random.choices(self.policies, weights=self.probs)[0](state, player, actions)

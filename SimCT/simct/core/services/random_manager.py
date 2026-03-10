"""Deterministic random manager placeholders."""

import random


class RandomManager:
    """Thin deterministic random wrapper for simulation services."""

    def __init__(self, seed: int = 42) -> None:
        self._rng = random.Random(seed)

    def randint(self, start: int, end: int) -> int:
        """Return deterministic integer in [start, end]."""
        return self._rng.randint(start, end)

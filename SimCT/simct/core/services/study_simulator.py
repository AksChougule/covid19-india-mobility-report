"""Study simulator placeholders."""

from collections.abc import Iterable

from simct.core.models.events import SimulationEvent
from simct.core.models.state import StudyState
from simct.core.services.random_manager import RandomManager


def simulate(
    initial_state: StudyState,
    events: Iterable[SimulationEvent],
    random_manager: RandomManager | None = None,
) -> StudyState:
    """Deterministic simulation placeholder that advances cycles by event count."""
    _ = random_manager
    event_count = sum(1 for _ in events)
    return initial_state.model_copy(update={"cycle": initial_state.cycle + event_count})

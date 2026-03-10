from simct.core.models.events import SimulationEvent
from simct.core.models.state import StudyState
from simct.core.services.study_simulator import simulate


def test_simulator_smoke_advances_cycle() -> None:
    state = StudyState(study_id="S1", cycle=0)
    next_state = simulate(state, [SimulationEvent(name="visit"), SimulationEvent(name="lab")])
    assert next_state.cycle == 2

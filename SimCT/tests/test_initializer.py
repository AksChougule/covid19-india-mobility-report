from simct.core.models.blueprint import StudyBlueprint
from simct.core.services.study_initializer import initialize_state


def test_initializer_creates_state() -> None:
    state = initialize_state(StudyBlueprint(study_id="S1"))
    assert state.study_id == "S1"

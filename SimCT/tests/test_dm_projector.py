from simct.core.models.state import StudyState
from simct.core.projectors.dm_projector import project_dm


def test_dm_projector_returns_dataframe() -> None:
    frame = project_dm(StudyState(study_id="S1"))
    assert "study_id" in frame.columns

from simct.core.models.state import StudyState
from simct.core.projectors.ae_projector import project_ae


def test_ae_projector_returns_dataframe() -> None:
    frame = project_ae(StudyState(study_id="S1"))
    assert "ae_count" in frame.columns

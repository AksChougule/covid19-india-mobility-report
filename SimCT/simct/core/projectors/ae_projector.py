"""AE projector placeholders."""

import pandas as pd

from simct.core.models.state import StudyState


def project_ae(state: StudyState) -> pd.DataFrame:
    """Create a minimal AE projection placeholder."""
    return pd.DataFrame([{"study_id": state.study_id, "ae_count": 0, "cycle": state.cycle}])

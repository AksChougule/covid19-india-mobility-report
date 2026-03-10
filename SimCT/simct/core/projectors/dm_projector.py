"""DM projector placeholders."""

import pandas as pd

from simct.core.models.state import StudyState


def project_dm(state: StudyState) -> pd.DataFrame:
    """Create a minimal DM projection placeholder."""
    return pd.DataFrame([{"study_id": state.study_id, "cycle": state.cycle}])

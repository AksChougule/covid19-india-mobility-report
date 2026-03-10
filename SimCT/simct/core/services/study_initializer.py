"""Study initializer placeholders."""

from simct.core.models.blueprint import StudyBlueprint
from simct.core.models.state import StudyState


def initialize_state(blueprint: StudyBlueprint) -> StudyState:
    """Create an initial study state from a blueprint."""
    return StudyState(study_id=blueprint.study_id)

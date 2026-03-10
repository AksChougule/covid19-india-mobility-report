"""Study validation placeholders."""

from simct.core.models.blueprint import StudyBlueprint


def validate_blueprint(blueprint: StudyBlueprint) -> list[str]:
    """Return placeholder validation errors for a blueprint."""
    _ = blueprint
    return []

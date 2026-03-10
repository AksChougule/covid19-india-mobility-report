"""Blueprint model placeholders."""

from typing import Any

from pydantic import BaseModel, Field


class StudyBlueprint(BaseModel):
    """Canonical loaded blueprint representation."""

    study_id: str = "placeholder-study"
    metadata: dict[str, Any] = Field(default_factory=dict)
    cohorts: list[dict[str, Any]] = Field(default_factory=list)

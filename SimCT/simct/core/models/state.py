"""Simulation state model placeholders."""

from typing import Any

from pydantic import BaseModel, Field


class StudyState(BaseModel):
    """Mutable study state snapshot."""

    study_id: str
    cycle: int = 0
    subjects: dict[str, Any] = Field(default_factory=dict)

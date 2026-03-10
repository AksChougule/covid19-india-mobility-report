"""Projection artifact model placeholders."""

from typing import Any

from pydantic import BaseModel, Field


class ProjectionArtifact(BaseModel):
    """Output artifact container."""

    artifact_type: str
    records: list[dict[str, Any]] = Field(default_factory=list)

"""Knowledge model placeholders."""

from typing import Any

from pydantic import BaseModel, Field


class KnowledgeGraph(BaseModel):
    """Resolved knowledge representation."""

    facts: dict[str, Any] = Field(default_factory=dict)

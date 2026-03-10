"""Simulation event model placeholders."""

from typing import Any

from pydantic import BaseModel, Field


class SimulationEvent(BaseModel):
    """Single event in the simulation timeline."""

    name: str
    payload: dict[str, Any] = Field(default_factory=dict)
    seed_offset: int = 0

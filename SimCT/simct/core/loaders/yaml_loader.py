"""YAML blueprint loader."""

from pathlib import Path
from typing import Any

import yaml

from simct.core.models.blueprint import StudyBlueprint


def load_blueprint(path: str | Path) -> StudyBlueprint:
    """Load a StudyBlueprint from YAML content."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        raw: Any = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raw = {}
    return StudyBlueprint.model_validate(raw)

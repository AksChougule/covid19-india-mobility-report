"""Public package API."""

from pathlib import Path

from simct.core.loaders.yaml_loader import load_blueprint
from simct.core.services.study_initializer import initialize_state


def load_study_blueprint(path: str | Path):
    """Load a study blueprint from YAML."""
    return load_blueprint(path)


def create_default_state(path: str | Path):
    """Create an initialized state from a blueprint path."""
    blueprint = load_study_blueprint(path)
    return initialize_state(blueprint)

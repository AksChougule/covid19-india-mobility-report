"""Knowledge resolution placeholders."""

from simct.core.models.blueprint import StudyBlueprint
from simct.core.models.knowledge import KnowledgeGraph


def resolve_knowledge(blueprint: StudyBlueprint) -> KnowledgeGraph:
    """Resolve input blueprint into a knowledge graph placeholder."""
    return KnowledgeGraph(facts={"study_id": blueprint.study_id})

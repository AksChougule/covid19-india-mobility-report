from simct.core.loaders.yaml_loader import load_blueprint


def test_blueprint_loader_reads_example() -> None:
    blueprint = load_blueprint("simct/examples/oncology_minimal.yaml")
    assert blueprint.study_id == "oncology-minimal"

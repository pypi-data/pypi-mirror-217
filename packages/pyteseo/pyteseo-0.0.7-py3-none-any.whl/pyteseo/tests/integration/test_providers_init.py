from pyteseo.providers.__init__ import (
    load_providers_datasets_registry,
    providers_registry_path,
)


def test_load_providers_datasets_registry():
    dataset_registry = load_providers_datasets_registry(providers_registry_path)
    assert "opendap" in dataset_registry.keys()
    assert len(dataset_registry["opendap"]) > 1
    assert "wfs" in dataset_registry.keys()
    assert len(dataset_registry["wfs"]) == 1

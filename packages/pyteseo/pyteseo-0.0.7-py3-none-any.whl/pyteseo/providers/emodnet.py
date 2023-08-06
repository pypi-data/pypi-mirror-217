from pyteseo.providers import DATASETS


def get_emodnet_opendap_urls(dataset_name) -> list:
    return DATASETS["opendap"]["emodnet"][dataset_name]["url"]

import pytest
from pyteseo.io.substances import (
    get_offline_substance,
    get_offline_substance_names,
    generate_substances_df,
)


@pytest.fixture
def json_response():
    return [
        {
            "name": "benceno",
            "id": 1,
            "uuid": "lkjasd6795a4",
            "data": {
                "k1": 1,
                "k2": 2,
                "k3": 3,
                "k4": 4,
                "k5": 5,
            },
            "metadata": {
                "creation_time": "2023-06-01T01:33:00Z",
                "created_by": "Pepe",
                "used_in_projects:": ["test_project_1", "test_project_2"],
                "used_in_domains": ["domain_3", "domain_4"],
            },
        },
        {
            "name": "etanol",
            "id": 1,
            "uuid": "lkjasd6795a4",
            "data": {
                "k1": 1,
                "k2": 2,
                "k3": 3,
                "k4": 4,
                "k5": 5,
            },
            "metadata": {
                "creation_time": "2023-06-01T01:33:00Z",
                "created_by": "Manolito",
                "used_in_projects:": ["test_project_1", "test_project_3"],
                "used_in_domains": ["domain_1", "domain_3"],
            },
        },
    ]


# NOTE - TO VALIDATE
def test_generate_substances_df(json_response):
    df_substances = generate_substances_df(json_response)
    assert len(df_substances) == len(
        set([substance["name"] for substance in json_response])
    )


@pytest.mark.parametrize(
    "substance_type, substance_name, exception",
    [
        ("oils", "lagunillas", FileNotFoundError),
        ("hns", "acetonas", ValueError),
    ],
)
def test_get_offline_substance_raises(substance_type, substance_name, exception):
    with pytest.raises(exception):
        df = get_offline_substance(substance_type, substance_name)
        assert df.name.values == substance_name


@pytest.mark.parametrize("substance_type", ["oil", "hns"])
def test_get_offline_substance_names(substance_type):
    substance_names = get_offline_substance_names(substance_type)
    assert len(substance_names) >= 1


def test_get_offline_substance_names_raises(
    substance_type="bad_name", exception=FileNotFoundError
):
    with pytest.raises(exception):
        _ = get_offline_substance_names(substance_type)

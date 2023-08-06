import pandas as pd
import xarray as xr

from shutil import copy2
from pathlib import Path

from pyteseo.io.forcings import write_2d_forcing
from pyteseo.preprocess.dataset import get_dataset
from pyteseo.preprocess.teseo_standarizations import standarize_dataset_varnames
from pyteseo.defaults import FILE_NAMES
from pyteseo.providers.connection import (
    get_provider_dataset,
    preprocess_online_provider,
    get_variable_map,
    DATASETS,
)

__all__ = ["create_forcings"]


def create_forcings(forcings, bbox, timebox, output_dir) -> tuple:
    print("\n")
    print(
        "\n------------------------------ PREPROCESSING TESEO FORCINGS ------------------------------"
    )
    print(
        "------------------------------------------------------------------------------------------\n"
    )
    forcings = preprocess_forcings_definition(forcings)
    model_timebox = list(timebox)

    for forcing_type, d in forcings.items():
        print(
            f"PREPROCESSING {forcing_type.upper()} [{d['dataset_name']}] FROM {d['source']}"
        )

        variable_map = d["variable_map"] if "variable_map" in d else None

        new_t_ini = create_forcing_from_provider(
            d["source"],
            d["dataset_name"],
            forcing_type,
            variable_map,
            output_dir,
            bbox,
            model_timebox,
        )
        if new_t_ini:
            if new_t_ini < timebox[0]:
                model_timebox[0] = new_t_ini
        print("done!\n")

    print(
        "--------------------------------------------------------------------------------------------"
    )
    print(
        "--------------------------------------------------------------------------------------------\n"
    )

    return tuple(model_timebox)


def preprocess_forcings_definition(forcings):
    def add_dt_h(forcings):
        for forcing_type, d in forcings.items():
            if "dt_h" not in d.keys():
                if (
                    "file_format" in d["source"]
                    and d["source"]["file_format"] == "netcdf"
                ):
                    raise ValueError(
                        f"Forcing time step ['dt_h'] not defined. check {forcing_type} definition [{d}]"
                    )
                elif (
                    "file_format" in d["source"]
                    and d["source"]["file_format"] == "teseo_txt"
                ):
                    raise ValueError(
                        f"Forcing time step ['dt_h'] not defined. check {forcing_type} definition [{d}]"
                    )
                elif "service" in d["source"] and d["source"]["service"] == "wfs":
                    raise ValueError(
                        f"Bad forcing configuration. check {forcing_type} definition [{d}]"
                    )
                dt_h = DATASETS[d["source"]["service"]][d["source"]["online_provider"]][
                    d["dataset_name"]
                ]["dt_h"]
                forcings[forcing_type]["dt_h"] = dt_h
        return forcings

    forcings = add_dt_h(forcings)
    return {
        key: forcings[key]
        for key in sorted(forcings, reverse=True, key=lambda x: forcings[x]["dt_h"])
    }


def create_forcing_from_provider(
    connection,
    dataset_name,
    dataset_type,
    variable_map,
    output_dir,
    bbox=None,
    timebox=None,
):
    if "online_provider" in connection.keys() and connection["service"] == "opendap":
        connection_params = preprocess_online_provider(
            connection["online_provider"], connection["service"], dataset_name
        )

        if not variable_map:
            variable_map = get_variable_map(
                connection["online_provider"], connection["service"], dataset_name
            )

        coordinates, variables = _split_variable_map(variable_map)

        ds = get_provider_dataset(
            connection_params,
            variables,
            bbox,
            timebox,
            coordinates[0],
            coordinates[1],
            coordinates[2],
        )
        dataset_to_teseo_txt(ds, output_dir, dataset_type, variable_map)
        return pd.Timestamp(ds[coordinates[0]][0].values).to_pydatetime()

    elif "local_path" in connection.keys() and connection["file_format"] == "netcdf":
        if not variable_map:
            raise ValueError(
                "variable_map not defined. Map like {'t': 'time', 'x': 'lon', 'y': 'lat', 'u': 'uwind', 'v': 'vwind'} is needed"
            )
        coordinates, variables = _split_variable_map(variable_map)
        ds = get_dataset(
            connection["local_path"],
            variables,
            bbox,
            timebox,
            coordinates[0],
            coordinates[1],
            coordinates[2],
        )
        dataset_to_teseo_txt(ds, output_dir, dataset_type, variable_map)
        return pd.Timestamp(ds[coordinates[0]][0].values).to_pydatetime()

    elif "local_path" in connection.keys() and connection["file_format"] in [
        "xlsx",
        "csv",
    ]:
        file_path = connection["local_path"]

        if connection["file_format"] == "xlsx":
            df = pd.read_excel(file_path)
        elif connection["file_format"] == "csv":
            df = pd.read_csv(file_path)
        else:
            raise ValueError(
                f"Bad forcing definition, check 'file_format' {connection}"
            )

        if len(df) == 1:
            # TODO - Write cte value forcing
            pass
        else:
            # TODO - Write timeseries forcing (spatially constant)
            pass

    elif "local_path" in connection.keys() and connection["file_format"] == "teseo_txt":
        copy_teseo_forcings(connection["local_path"], dataset_type, output_dir)

    elif "set_cte_value" in connection.keys():
        # TODO - Create dataframe forcing variables
        # TODO - Write cte value forcing
        pass
    else:
        raise ValueError("Bad forcing definition")


def dataset_to_teseo_txt(
    ds: xr.Dataset, output_dir: str, forcing_type: str, variable_map: dict
) -> None:
    """preprocess xarray dataset to TESEO's txt format

    Args:
        ds (xr.Dataset): source dataset
        output_dir (str): folder where txt-files where created
        forcing_type (str): ["currents", "winds", "waves", "currents_depthavg"]
        variable_map (dict): defined as {key: source_varname}. ["t", "x", "y", "u", "v", "hs", "dir", "tp"]
    """
    ds = standarize_dataset_varnames(ds, forcing_type, variable_map)
    print("Converting data to pd.DataFrame...")
    df = ds.to_dataframe().reset_index()
    df["time"] = (df["time"] - df["time"][0]).dt.total_seconds() / 3600
    print("Writing data to teseo-txt files...")
    write_2d_forcing(df, output_dir, forcing_type)


def copy_teseo_forcings(file_paths: list, forcing_type: str, output_dir: str):
    lst = []

    for file in file_paths:
        path = Path(file)
        new_path = Path(output_dir, path.name)
        copy2(file, new_path)
        lst.append(str(new_path.name) + "\n")

    with open(Path(output_dir, FILE_NAMES[forcing_type]), "w") as f:
        f.writelines(lst)


def _split_variable_map(
    variable_map: dict, coords: list = ["t", "x", "y", "z"]
) -> tuple:
    coordinates = [v for k, v in variable_map.items() if k in coords]
    variables = [v for k, v in variable_map.items() if k not in coords]
    return coordinates, variables

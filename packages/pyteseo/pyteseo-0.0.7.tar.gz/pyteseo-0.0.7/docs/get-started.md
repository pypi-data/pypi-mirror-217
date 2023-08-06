# Get started
Quickstart guide to use pyTESEO

---

## Installation
1. Install the python library using pip:

```bash
# From pypi repository
pip install pyteseo

# Or directly from github repository
pip install git+https://github.com/IHCantabria/pyteseo
```

2. Install TESEO model binary (**Not available yet!**):
- Get access to the binary @ (https://github.com/IHCantabria/TESEO/blob/main/bin)
- Set up environment variable "TESEO_PATH" with the path to the model executable. You can use the command following CLI command after activate the python environement (python-dotenv library)

    ```bash
        dotenv set TESEO_PATH /path/to/teseo_executable
    ```

3. Online data providers requires to stablish opendap connections that requires in some casess aditional configurations:

    * [CMEMS products](https://data.marine.copernicus.eu/products) requires authentication. You should set up the environment variables `CMEMS_username` and `CMEMS_password`.
    ```bash
    dotenv set CMEMS_username your_username_at_CMEMS
    ```
    ```bash
    dotenv set CMEMS_password your_password_at_CMEMS
    ```

    * [IHCantabria products](https://discoverymap.ihcantabria.com/) requires connection to IHCantabria datahub API. You should set up the environment variable `DATAHUB_API_URL`.
    ```bash
    DATAHUB_API_URL = "https://datahub.ihcantabria.com"
    ```

---

Tests are located in `pyteseo/tests/` and data required for tests are located in `pyteseo/tests/data/`.
Tests have been developed using [pytest](https://docs.pytest.org/).

Run tests to verify your installation, it is widely recommended:
```bash
pyteseo-test        # Run tests and prompt pytest-report
```

---

## Main functionalities
See [TL:DR guide](./tl;dr-guide.md) section to get quick-examples about:
- Create a TESEO domain
- Create forcings for TESEO
- Create a TESEO simulation
- Export TESEO simulation results to standard formats
- Perform basic plots

---

## Use cases
```{error}
To be completed!

```
Some use cases have been developed as an examples of use of this package.
All the use cases are provided as notebooks (*.ipynb) in the source code repository under the path `docs/notebooks`. Moreover, all the notebooks include a link to be opened and executed in `Google Colab`.

Check **USE CASES** section at left panel to access them.

## Package under development!
---

<p align="center">
<img align="center" width="600" src="https://ihcantabria.github.io/pyteseo/_images/pyTESEO_logo.png">
</p>

[![pypi](https://img.shields.io/pypi/v/pyteseo)](https://pypi.org/project/pyteseo/)
[![Github release (latest by date)](https://img.shields.io/github/v/release/ihcantabria/pyteseo?label=last%20release)](https://github.com/IHCantabria/pyteseo/releases)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/IHCantabria/pyteseo?label=last%20tag)](https://github.com/IHCantabria/pyteseo/tags)
[![GitHub last commit](https://img.shields.io/github/last-commit/ihcantabria/pyteseo)](https://github.com/IHCantabria/pyteseo/commits/main)
[![docs](https://github.com/IHCantabria/pyteseo/actions/workflows/docs.yml/badge.svg)](https://github.com/IHCantabria/pyteseo/actions/workflows/docs.yml)
[![tests](https://github.com/IHCantabria/pyteseo/actions/workflows/tests.yml/badge.svg)](https://github.com/IHCantabria/pyteseo/actions/workflows/tests.yml)
[![GitHub repo size](https://img.shields.io/github/repo-size/IHCantabria/pyteseo)](https://github.com/IHCantabria/pyteseo)
[![GitHub license](https://img.shields.io/github/license/IHCantabria/pyteseo)](https://github.com/IHCantabria/pyteseo/blob/main/LICENSE.md)
[![Python versions](https://img.shields.io/pypi/pyversions/pyteseo)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



**pyTESEO** is a python package developed by [IHCantabria](https://ihcantabria.com/en/) to simplify and facilitate the setup and processing of [TESEO](https://ihcantabria.com/en/specialized-software/teseo/) simulations *(TESEO is a lagrangian numerical model also developed by IHCantabria.)*


---

## 💻 Installation

1. Install pyTESEO library:

    [Pip package manager](https://pip.pypa.io/en/stable/) is needed to install the library and
    it is recommended to be installed from [IHCantabria/pyteseo](https://github.com/IHCantabria/    pyteseo) repository:
    ```bash
    pip install git+https://github.com/IHCantabria/pyteseo
    ```

    *Alternatively, you can install it from pypi but you will need also install some direct dependencies     that are not publish in pipy repositories:*
    ```bash
    pip install pyteseo

    # direct dependencies:
    pip install "datahub @ https://github.com/IHCantabria/datahub.client/archive/refs/tags/v0.9.4.zip"
    ```

2. Install TESEO model binary (**Not available yet!**):

    - Get access to the binary @ (https://github.com/IHCantabria/TESEO/blob/main/bin)
    - Set up environment variable "TESEO_PATH" with the path to the model executable. You can use the   command following CLI command after activate the python environement (python-dotenv library)

        ```bash
            dotenv set TESEO_PATH /path/to/teseo_executable
        ```

3. Online data providers require to stablish opendap connections, and in some cases aditional configurations:

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

## ✔️ Tests
Tests are located in `pyteseo/tests/` and data required for tests are located in `pyteseo/tests/data/`.
Tests have been developed using [pytest](https://docs.pytest.org/).

Run tests to verify your package installation:
```bash
pyteseo-test        # Run tests and prompt pytest-report
```

---

## ♻️ Continuous integration (CI)

* Build and deploy documentation on Github Pages in [.github/workflows/docs.yml](.github/workflows/docs.yml)
* Install and test package in diferent environments in [.github/workflows/tests.yml](.github/workflows/tests.yml)
* Precommit hooks for formats and linting in [.pre-commit-config.yaml](.pre-commit-config.yaml)

*For Linux, Windows, MacOS and compatible python versions defined in installation section*

---

## 📚 Documentation

Documentation is available at https://ihcantabria.github.io/pyteseo

---

## ©️ Credits
Developed and maintained by 👨‍💻 [German Aragon](https://github.com/aragong) @ 🏢 [IHCantabria](https://github.com/IHCantabria).

---

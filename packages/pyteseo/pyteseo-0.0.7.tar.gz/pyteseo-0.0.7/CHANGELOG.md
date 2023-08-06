# Changelog

## v0.0.8 - ??/??/2023
### Added:
1)
2)
3)
4)
5)
### Changed:
1)
2)
3)
### Fixed:
1)
2)
3)
<br/><br/>


## v0.0.7 - 05/07/2023
### Added:
1) preprocessing from any netcdf to teseo netcdf
2) create_forcings
3) create_domain
4) create_simulation
5) TL;DR guide added to docs
### Changed:
1) up for python>=3.8
2) update documentation
3) update testing
### Fixed:
1) login CMEMS was trigger at each operation
2)
3)
<br/><br/>


## v0.0.6 - 23/05/2023
### Added:
1) Classes for forcings
2) Create null forcings
3) Create TeseoWrapper class
4) Create cfg and run files
5) Create *_hns.calib file
6) First integration tests runing teseo v1.2.8 (drifter, oil and hns) with cte forcings with and without coastline
7) Add general attributes to netcdf results
8) Run simulations with 2d forcings (winds and currents)
9) Add plot package with basic plots, figures and animations
### Changed:
1) modules are getting too big, I split structure into subpackages
2) generalize i/o of forcings to spatially cte or 2d
3) downgrade netcdf version to hotfix netcdf library bug introduced in new versions
4) notebooks will not be a priority from now on
### Fixed:
1) notebooks to run documentation ci
2) access CMEMS from the notebooks (github secret)
3) Tests in github actions (downgrade netcdf. netcdf problem, not us!)
<br/><br/>


## v0.0.5 - 19/01/2023
### Added:
1) read results (particles, properties, and grids)
2) add mod calculation to read_currents and read_winds
3) notebook 02
4) add py3.11 to test workflow
5) exclude windows w/ py3.7
6) add pyteseo.export functionality
7) add pyteseo/defaults.json to centralize defaults (names, configs...)
8) add docs/notebooks/03_export_resutls.ipynb
### Changed:
1) cli pyteseo-tests move to pyteseo/tests.__init__.py
### Fixed:
1) added pre-commit with check-yaml, end-of-file-fixer, trailing-whitespace, black, black-jupyter and falke8
<br/><br/>


## v0.0.4 - 11/01/2023
### Added:
1) required version pytest >=7
### Changed:
### Fixed:
1) relative paths to pyteseo installtion for notebooks
<br/><br/>


## v0.0.3 - 11/01/2023
### Added:
1) add google colab for notebooks
### Changed:
1) update python version requirement to 3.7
### Fixed:
1) Compatibility for python versions >=3.7
<br/><br/>


## v0.0.2 - 11/01/2023
### Added:
1) coverage functionality
2) tools configuration in pyproject.toml
3) write currents and winds with io module
4) build and publish in pypi.test
5) build and publish in pypi
6) user able to use tests to validate installation
7) add jupyter notebooks in docs
8) publish docs in github repo page-service
### Changed:
1) upgrade logic for coastlines
2) change structure to add tests as subpackage
3) update doc
4) visibility of the repo to public
### Fixed:
1) None
<br/><br/>


## v0.0.1 - 29/12/2022
### Added:
1) Init repository using flit
2) Initial structure of the package
3) Functions read_grid, read_coastline, write_grid, write_coastline in pyteseo.io.py
4) Testing using pytest
5) Initial documentation using sphynx, myst_parser, autoapi...
6) Logo images for TESEO and pyTESEO
7) First CHANGELOG
### Changed:
1) None
### Fixed:
1) None
<br/><br/>

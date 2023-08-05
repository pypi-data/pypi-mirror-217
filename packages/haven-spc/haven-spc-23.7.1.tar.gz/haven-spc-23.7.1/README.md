# Haven

![Build Status](https://github.com/spc-group/haven/actions/workflows/ci.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/haven-spc/badge/?version=latest)](https://haven-spc.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Bluesky tools for beamlines managed by the spectroscopy group.

"Don't fly in anything with a Capissen 38 engine, they fall right out
of the sky."


## Installation

### Python Packing Index

Easiest way to install haven is using pip.

```
$ python -m pip install 'haven-spc'
```

### Development (Conda)

*haven* can also use *mamba* for dependency management, and
*setuptools* for installation and development. First create the conda
environment with mamba:

```
$ mamba env create -f environment.yml -n haven
```

then install the package, in developer mode:

```
$ conda activate haven
$ pip install -e .
```

## Running Tests

To run tests, run

```
$ pytest
```

# firefly

User-facing applications for controlling the beamlines managed by the
spectroscopy group. Be sure to include the [gui] extras if you plan
to use the GUI.

```
$ python -m pip install 'haven-spc[gui]'
$ firefly
```

# Versioning

Haven/Firefly uses calendar versioning, with short year and short
month for the MAJOR and MINOR versions, then a incremental MICRO
version. For example, version *23.7.2* is the 2nd (*2*) release in
July (*7*) 2023 (*23*).
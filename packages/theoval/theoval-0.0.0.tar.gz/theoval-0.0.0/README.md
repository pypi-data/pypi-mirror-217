# Theoval

[![PyPI](https://img.shields.io/pypi/v/theoval.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/theoval.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/theoval)][python version]
[![License](https://img.shields.io/pypi/l/theoval)][license]

[![Read the documentation at https://theoval.readthedocs.io/](https://img.shields.io/readthedocs/theoval/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/jderiu/theoval/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/jderiu/theoval/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/theoval/
[status]: https://pypi.org/project/theoval/
[python version]: https://pypi.org/project/theoval
[read the docs]: https://theoval.readthedocs.io/
[tests]: https://github.com/jderiu/theoval/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/jderiu/theoval
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- TODO

## Requirements

All requirements are listed in the [package description file](pyproject.toml).

## Installation

You can install _Theoval_ via [pip] from [PyPI]:

```console
$ pip install theoval
```

## Usage

### Command Line Usage

Display help:
```console
python -m theoval --help

Usage: theoval [OPTIONS]

Options:
  --version                       Show the version and exit.
  -e, --etype [binary|preference]
                                  [required]
  -i, --input_data TEXT           [required]
  -o, --output_path TEXT          [required]
  -m, --metrics TEXT
  -s, --systems TEXT
  --help                          Show this message and exit.
```

We provide example data for both binary and preference based evaluation:
* [binary example data](examples/binary/data/wmt_data.jsonl)
* [preference example data](examples/preference/data/wmt_data.jsonl)


## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Theoval_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/jderiu/theoval/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/jderiu/theoval/blob/main/LICENSE
[contributor guide]: https://github.com/jderiu/theoval/blob/main/CONTRIBUTING.md
[command-line reference]: https://theoval.readthedocs.io/en/latest/usage.html

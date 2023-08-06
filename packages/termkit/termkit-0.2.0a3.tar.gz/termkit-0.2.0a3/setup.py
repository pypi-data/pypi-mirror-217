# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termkit']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'termkit',
    'version': '0.2.0a3',
    'description': 'Command Line Tools with ease',
    'long_description': '<p align="center">\n    <img alt="Termkit" title="Termkit" src="docs/images/banner.png#gh-dark-mode-only" width="450">\n    <img alt="Termkit" title="Termkit" src="docs/images/banner_light.png#gh-light-mode-only" width="450">\n</p>\n<div align="center">\n  <b><i>Command Line Tools with... ease.</i></b>\n<hr>\n\n[![Tests](https://github.com/thmahe/termkit/actions/workflows/tests.yml/badge.svg)](https://github.com/thmahe/termkit/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/github/thmahe/termkit/branch/master/graph/badge.svg?token=o7UVrOsoq4)](https://codecov.io/github/thmahe/termkit)\n![PyPI](https://img.shields.io/pypi/v/termkit)\n![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20MacOS%20%7C%20Windows-lightgrey)\n\n</div>\n\n## Table of Contents\n\n- [Introduction](#introduction)\n- [Features](#features)\n- [Requirement](#requirement)\n- [Installation](#installation)\n- [Examples](#examples)\n- [Feedback](#feedback)\n- [Acknowledgments](#acknowledgments)\n\n## Introduction\n\nTermkit is a framework for building command line interface applications using functions \nand type hints [[PEP 484]](https://peps.python.org/pep-0484/). \n**Solely written using [Python Standard Library](https://docs.python.org/3/library/)** and will always be to ensure\nminimal dependency footprint within your project.\n\nIn few words, Termkit is designed to be the foundation of serious CLI tools.\n\n## Features\n\nA few of the things you can do with Termkit:\n\n* Build CLI from functional code\n* Create fast prototypes using implicit arguments\n* Helpers populated from docstrings\n* Named profile for pre-populated arguments\n* Autocompletion through [argcomplete](https://pypi.org/project/argcomplete/) module\n* Cross-platforms\n\n## Requirement\n* Python 3.7 or higher\n\n*Yes... that\'s about it !* \n\n### Compatibility matrix\n\n|          OS | Python 3.6 |     Python 3.7     |     Python 3.8     |     Python 3.9     |    Python 3.10     |    Python 3.11     |    Python 3.12    |\n|------------:|:----------:|:------------------:|:------------------:|:------------------:|:------------------:|:------------------:|:-----------------:|\n|   **Linux** |    :x:     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_plus_sign: |\n|   **MacOS** |    :x:     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_plus_sign: |\n| **Windows** |    :x:     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_plus_sign: |\n\n\n## Installation\n\nTermkit is published as a [Python package](https://pypi.org/project/termkit) and can be installed with pip.\n\nOpen up a terminal and install Termkit with:\n```shell\npip install termkit\n```\n\n## Examples\n\n### Greeting application\n\n```python\n# greet.py\nimport termkit\n\ndef greet(name):\n    print(f\'Hello {name} !\')\n\nif __name__ == \'__main__\':\n    termkit.run(greet)\n```\n\n```\n$ python3 ./greet.py Thomas\nHello Thomas !\n```\n\n## Feedback\n\nFeel free to send me feedback by [raising an issue](https://github.com/thmahe/termkit/issues/new).\nFeature requests are always welcome.\n\n',
    'author': 'Thomas Mahé',
    'author_email': 'contact@tmahe.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

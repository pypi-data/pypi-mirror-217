# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['code_var']

package_data = \
    {'': ['*']}

install_requires = \
    [
        "bs4==0.0.1",
        "requests==2.28.1",
        "typer==0.6.1"
    ]

entry_points = \
    {'console_scripts': ['vn = code_var.cli:run']}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_kwargs = {
    'name': 'code_var',
    'version': '0.1.3',
    'description': '"code-var is tools for varname in cmd"',
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    'author': 'JackCCC',
    'maintainer': None,
    'maintainer_email': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}

setup(**setup_kwargs)

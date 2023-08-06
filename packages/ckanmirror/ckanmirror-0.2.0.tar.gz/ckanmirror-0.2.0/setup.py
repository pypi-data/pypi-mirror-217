# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ckanmirror']

package_data = \
{'': ['*']}

install_requires = \
['ckanapi>=4.7,<5.0',
 'humanize>=4.7.0,<5.0.0',
 'requests>=2.31.0,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

entry_points = \
{'console_scripts': ['ckanmirror = ckanmirror.cli:cli']}

setup_kwargs = {
    'name': 'ckanmirror',
    'version': '0.2.0',
    'description': '',
    'long_description': "# ckanmirror\n\nA simple command-line utility that enables incremental mirroring of a nominated package\nfrom a CKAN instance. All CKAN resources associated with the package will be downloaded,\nalong with their associated metadata. Resources linked from previous versions of the package\nare not changed, so this tool can be used to build up an archive of a CKAN package over time.\n\n## Getting started\n\nInstall the tool:\n\n```\npip install ckanmirror\n```\n\nIn a directory you wish the CKAN package to be mirrored to, write your config into a file named `ckanmirror.json`:\n\n```\n{\n    'apikey': '<your CKAN API key>',\n    'remote': 'https://ckan.example.com',\n    'package_id': '<CKAN package ID>',\n\n}\n```\n\n... then, from that directory, simply run `ckanmirror`.\n\n",
    'author': 'Grahame Bowland',
    'author_email': 'grahame@bowland.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

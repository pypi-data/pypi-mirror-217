# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparsenn']

package_data = \
{'': ['*']}

install_requires = \
['equinox>=0.10.6,<0.11.0', 'jax>=0.4.13,<0.5.0', 'optax>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'sparsenn',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Jeff Shen',
    'author_email': 'shenjeff@princeton.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

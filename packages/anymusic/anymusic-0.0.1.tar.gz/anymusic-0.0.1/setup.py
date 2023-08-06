# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anymusic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'anymusic',
    'version': '0.0.1',
    'description': 'Music from the very basic.',
    'long_description': '# AnyMusic\n\n*Music from the very basic.*\n\nAnyMusic aims to provide a set of tools to make programmatic sounds that are more generalized.\n',
    'author': 'Yi Cao',
    'author_email': 'me@ycao.top',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

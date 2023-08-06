# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tripp']

package_data = \
{'': ['*']}

install_requires = \
['mdanalysis>=2.5.0,<3.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.0.3,<3.0.0',
 'propka>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'tripp',
    'version': '0.1.1',
    'description': 'Trajectory Iterative pKa Predictor',
    'long_description': '',
    'author': 'Christos Matsingos',
    'author_email': 'c.matsingos@qmul.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

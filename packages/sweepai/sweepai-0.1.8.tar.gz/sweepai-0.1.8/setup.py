# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sweepai', 'sweepai.app', 'sweepai.core', 'sweepai.handlers', 'sweepai.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub==1.58.2',
 'config-path>=1.0.3,<2.0.0',
 'fastapi>=0.94.1,<0.95.0',
 'gradio>=3.35.2,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'requests>=2.28.2,<3.0.0',
 'urllib3>=2.0.3,<3.0.0',
 'uvicorn>=0.21.0,<0.22.0']

entry_points = \
{'console_scripts': ['sweep = sweepai.app.cli:app',
                     'sweepai = sweepai.app.cli:app']}

setup_kwargs = {
    'name': 'sweepai',
    'version': '0.1.8',
    'description': 'Sweep software chores',
    'long_description': None,
    'author': 'Kevin Lu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

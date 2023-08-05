# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sweepai', 'sweepai.app', 'sweepai.core', 'sweepai.handlers', 'sweepai.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.31,<4.0.0',
 'PyGithub==1.58.2',
 'PyJWT>=2.6.0,<3.0.0',
 'anthropic>=0.2.8,<0.3.0',
 'backoff>=2.2.1,<3.0.0',
 'build>=0.10.0,<0.11.0',
 'chromadb>=0.3.21,<0.4.0',
 'config-path>=1.0.3,<2.0.0',
 'diskcache>=5.6.1,<6.0.0',
 'docarray>=0.21.0,<0.22.0',
 'fastapi>=0.94.1,<0.95.0',
 'flake8>=6.0.0,<7.0.0',
 'google-search-results>=2.4.2,<3.0.0',
 'gradio>=3.35.2,<4.0.0',
 'highlight-io==0.5.0',
 'loguru>=0.6.0,<0.7.0',
 'modal-client>=0.49.2348,<0.50.0',
 'nptyping>=2.5.0,<3.0.0',
 'openai>=0.27.2,<0.28.0',
 'posthog>=3.0.1,<4.0.0',
 'pre-commit>=3.2.0,<4.0.0',
 'pymongo>=4.4.0,<5.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'redis>=4.5.5,<5.0.0',
 'requests>=2.28.2,<3.0.0',
 'slack-bolt>=1.18.0,<2.0.0',
 'slack-sdk>=3.21.3,<4.0.0',
 'tiktoken>=0.3.2,<0.4.0',
 'tree-sitter>=0.20.1,<0.21.0',
 'types-requests>=2.28.11.15,<3.0.0.0',
 'urllib3>=2.0.3,<3.0.0',
 'uvicorn>=0.21.0,<0.22.0']

entry_points = \
{'console_scripts': ['sweep = sweepai.app.cli:app',
                     'sweepai = sweepai.app.cli:app']}

setup_kwargs = {
    'name': 'sweepai',
    'version': '0.1.7',
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

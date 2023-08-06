# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neptune_airflow', 'neptune_airflow.impl']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit', 'pytest>=5.0', 'pytest-cov==2.10.1', 'neptune>=1.0.0']}

setup_kwargs = {
    'name': 'neptune-airflow',
    'version': '0.0.0',
    'description': 'Neptune.ai airflow integration library',
    'long_description': '# Neptune - airflow integration\n\nTODO: Update docs link\nSee [the official docs](https://docs.neptune.ai/integrations-and-supported-tools/model-training/).',
    'author': 'neptune.ai',
    'author_email': 'contact@neptune.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://neptune.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

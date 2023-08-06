# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongtic']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[dotenv,email]>=1.10.6,<2.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'pymongtic',
    'version': '0.1.0',
    'description': 'A simple object data mapping that uses Pydantic and pymongo to simplify integrating MongoDB with Pydantic and FastAPI',
    'long_description': '# pymongtic\n\nSimple pymongo ODM that uses pydantic for validation\n',
    'author': 'Paul J DeCoursey',
    'author_email': 'paul@decoursey.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

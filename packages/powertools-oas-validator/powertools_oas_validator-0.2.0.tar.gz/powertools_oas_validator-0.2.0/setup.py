# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powertools_oas_validator', 'powertools_oas_validator.services']

package_data = \
{'': ['*']}

install_requires = \
['aws-lambda-powertools>=2.18.0,<3.0.0',
 'chocs-middleware-openapi>=1.2.2,<2.0.0',
 'fastjsonschema>=2.17.1,<3.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'openapi-spec-validator>=0.5.7,<0.6.0']

setup_kwargs = {
    'name': 'powertools-oas-validator',
    'version': '0.2.0',
    'description': '',
    'long_description': '# powertools-oas-validator',
    'author': 'Rasmus Hansen',
    'author_email': 'Rasmus.Hansen@LifeWorks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

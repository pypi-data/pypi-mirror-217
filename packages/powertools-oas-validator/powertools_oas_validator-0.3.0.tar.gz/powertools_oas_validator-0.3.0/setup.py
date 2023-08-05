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
    'version': '0.3.0',
    'description': '',
    'long_description': '# powertools-oas-validator\n<br>[![PyPI version](https://badge.fury.io/py/powertools-oas-validator.svg)](https://pypi.org/project/powertools-oas-validator/) ![Release](https://github.com/RasmusFangel/powertools-oas-validator/workflows/Publish/badge.svg) ![CI](https://github.com/RasmusFangel/powertools-oas-validator/workflows/CI/badge.svg)\n\n## Introduction\n\n[Powertools for AWS Lambda (Python)](https://github.com/aws-powertools/powertools-lambda-python) is an awesome set of tools for supercharging your lambdas. Powertools supports validating incoming requests (or event in PT lingo) against [JSONSchema](https://json-schema.org/) which is not ideal if you are using OpenAPI schemas to define your API contracts.\n\nThe *Powertools OAS Validator* adds a decorator that you can use with your lambda handlers and have the events validated against an OpenAPI schema instead.\n\n\n## Usage\nDecorate your functions with `@validate_request(oas_path="openapi.yaml")` and your request (and schema) will be validated on a request.\n\nSchema validation is enabled per default but can be disabled if you already validate your schema (perhaps as part of a pipeline)\n\n### Minimal Example\n\n```python\nfrom typing import Dict\nfrom aws_lambda_powertools.event_handler import APIGatewayRestResolve, Rresponse\nfrom aws_lambda_powertools.utilities.typing import LambdaContext\nfrom aws_lambda_powertools.middleware import validate_request\n\n\napp = APIGatewayRestResolver()\n\n@app.post("/example")\ndef example() -> Response:\n  ...\n\n@validate_request(oas_path="openapi.yaml")\ndef lambda_handler(event: Dict, context: LambdaContext) -> Dict:\n    response = app.resolve(event, context)\n\n    return response\n```\n\n\n### Extended Example\n```python\nfrom typing import Dict\nfrom aws_lambda_powertools.event_handler import APIGatewayRestResolve, Rresponse\nfrom aws_lambda_powertools.utilities.typing import LambdaContext\nfrom aws_lambda_powertools.middleware import validate_request\n\n\napp = APIGatewayRestResolver()\n\n@app.post("/example")\ndef example() -> Response:\n  ...\n\n@validate_request(\n  oas_path="openapi.yaml",\n  validate_spec=True,  # default True, disable to not validate OpenAPI Schema\n  validate_body=True,  # default True, disable to not validate event["body"] \n  validate_headers=True,  # default True, disable to not validate event["headers"]\n  validate_query=True,  # default True, disable to not validate event["rawQueryString"]\n  validate_path=True,  # default True, disable to not validate path parameters\n  validate_cookies=True, # default True, disable to not validate cookies\n\n)\ndef lambda_handler(event: Dict, context: LambdaContext) -> Dict:\n    response = app.resolve(event, context)\n\n    return response\n```\n\n',
    'author': 'Rasmus Hansen',
    'author_email': 'R.FangelHansen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

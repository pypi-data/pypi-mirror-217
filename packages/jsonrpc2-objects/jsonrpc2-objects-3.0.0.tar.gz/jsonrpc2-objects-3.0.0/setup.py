# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonrpcobjects']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pydantic>=2.0,<3.0']

setup_kwargs = {
    'name': 'jsonrpc2-objects',
    'version': '3.0.0',
    'description': 'A collection of objects for use in JSON-RPC 2.0 implementations.',
    'long_description': '# JSON-RPC 2.0 Objects\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://mit-license.org/)\n\nA collection of objects for use in JSON-RPC 2.0 implementations.\n\n## Installation\n\n```shell\npoetry add jsonrpc2-objects\n```\n\n```shell\npip install jsonrpc2-objects\n```\n\n## Objects\n\nAvailable in `objects` are the following:\n\n| Object             | Description                 |\n|--------------------|-----------------------------|\n| ParamsRequest      | Request with params         |\n| Request            | Request without params      |\n| ParamsNotification | Notification with params    |\n| Notification       | Notification without params |\n| ErrorResponse      | Response with result        |\n| ResultResponse     | Response with error         |\n\n## Errors\n\nPython exceptions are available for each JSON-RPC 2.0 error. Each error\nextends `JSONRPCError`.\n\n- JSONRPCError\n- InternalError\n- InvalidParams\n- InvalidRequest\n- MethodNotFound\n- ParseError\n- ServerError\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/jsonrpc2-objects',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grpc_gateway']

package_data = \
{'': ['*']}

install_requires = \
['pait[grpc]==1.0.0a6', 'protobuf-to-pydantic>=0.1.7.3,<0.2.0.0']

extras_require = \
{'template': ['jinja2>=2.0.0']}

entry_points = \
{'console_scripts': ['protoc-gen-route = '
                     'grpc_gateway.protobuf_plugin.main:main']}

setup_kwargs = {
    'name': 'grpc-gateway',
    'version': '0.0.1',
    'description': 'Python gRPC Gateway',
    'long_description': '',
    'author': 'so1n',
    'author_email': 'so1n897046026@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/python-pai/grpc-gateway',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

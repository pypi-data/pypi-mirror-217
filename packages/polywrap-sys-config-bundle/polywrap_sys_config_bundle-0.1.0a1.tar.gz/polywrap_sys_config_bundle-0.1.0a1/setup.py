# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_sys_config_bundle',
 'polywrap_sys_config_bundle.embeds',
 'polywrap_sys_config_bundle.types']

package_data = \
{'': ['*'],
 'polywrap_sys_config_bundle.embeds': ['file-system-resolver/*',
                                       'http-resolver/*']}

install_requires = \
['polywrap-client-config-builder>=0.1.0a1,<0.2.0',
 'polywrap-core>=0.1.0a1,<0.2.0',
 'polywrap-fs-plugin>=0.1.0a1,<0.2.0',
 'polywrap-http-plugin>=0.1.0a1,<0.2.0',
 'polywrap-manifest>=0.1.0a1,<0.2.0',
 'polywrap-uri-resolvers>=0.1.0a1,<0.2.0',
 'polywrap-wasm>=0.1.0a1,<0.2.0']

setup_kwargs = {
    'name': 'polywrap-sys-config-bundle',
    'version': '0.1.0a1',
    'description': 'Polywrap System Client Config Bundle',
    'long_description': '# polywrap-test-cases\n\nThis package allows fetching wrap test-cases from the wrap-test-harness.\n',
    'author': 'Niraj',
    'author_email': 'niraj@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

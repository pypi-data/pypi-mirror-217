# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wsuks', 'wsuks.helpers']

package_data = \
{'': ['*'], 'wsuks': ['executables/*', 'xml_files/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'impacket>=0.10.0,<0.11.0',
 'scapy>=2.5.0,<3.0.0',
 'termcolor>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['wsuks = wsuks.wsuks:main']}

setup_kwargs = {
    'name': 'wsuks',
    'version': '0.2.0',
    'description': 'A Tool for automating the MITM attack on the WSUS connection',
    'long_description': '# wsuks\nTBD\n',
    'author': 'Alexander Neff',
    'author_email': 'alex99.neff@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

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
    'version': '0.2.1',
    'description': 'A Tool for automating the MITM attack on the WSUS connection',
    'long_description': '![Supported Python versions](https://img.shields.io/badge/python-3.10+-blue.svg) [![Twitter](https://img.shields.io/twitter/follow/al3x_n3ff?label=al3x_n3ff&style=social)](https://twitter.com/intent/follow?screen_name=al3x_n3ff)\n# wsuks\n_Weaponizing the WSUS Attack_\n\nBecoming local Admin on a domain joined Windows Machine is usually the first step to obtain domain admin privileges in a pentest. To utilize the WSUS attack automatically this Tool spoofs the ip address of the WSUS-Server inside the network via arp and serves its own Windows Update as soon as the client requests them.\nPer Default a Windows Client requests Updates every 24h. On request wsuks provides its own "Updates" executing Powershell commands on the target to create an local Admin and add it to the local Administrators group.\n\nThe served executable (Default: PsExec64.exe) as well as the executed command can be changed as needed.\n\n## Installation\nUsing pipx:\n```\nsudo apt install python3-pipx git\nsudo pipx ensurepath\nsudo pipx install wsuks\n```\n\nUsing poetry:\n```\nsudo apt install python3-poetry\ngit clone https://github.com/NeffIsBack/wsuks\ncd wsuks\nsudo poetry install\n```\n\n## Usage\n❗wsuks must be run as root❗\n\nWith pipx:\n```\nsudo -i\nwsuks\nwsuks -t 10.0.0.10 --WSUS-Server 10.0.0.20\n```\n\nWith poetry:\n```\nsudo poetry run wsuks\nsudo poetry run wsuks -t 10.0.0.10 --WSUS-Server 10.0.0.20\n```\n\n## About & Mitigation\nIn the [PyWSUS](https://github.com/GoSecure/pywsus) Repository from GoSecure you can find a great documentation how to you could detect and mitigate this attack.\nThey also wrote a great Guide demonstrating how this attack works in detail [here](https://www.gosecure.net/blog/2020/09/03/wsus-attacks-part-1-introducing-pywsus/).\n\nThis Tool is based on the following projects:\n- https://github.com/GoSecure/pywsus\n- https://github.com/GoSecure/wsuspect-proxy\n\n',
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

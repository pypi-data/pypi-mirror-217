# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kade_drive',
 'kade_drive.core',
 'kade_drive.message_system',
 'kade_drive.tests']

package_data = \
{'': ['*']}

install_requires = \
['netifaces==0.11.0', 'rpyc==5.3.1', 'typer==0.9.0']

setup_kwargs = {
    'name': 'kade-drive',
    'version': '0.1.0',
    'description': 'distributed file system based on kademlia dht',
    'long_description': 'Sistema de ficheros distribuidos immplementado usando el codigo fuente de la implementacion de Kademlia en https://github.com/bmuller/kademlia \n\n### Tests\nPara Correr los tests se requiere un servidor levantado en la red',
    'author': 'DanielUH2019',
    'author_email': 'danielcardenascabrera2016@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sport_activities_features_gui',
 'sport_activities_features_gui.logic',
 'sport_activities_features_gui.models',
 'sport_activities_features_gui.widgets',
 'sport_activities_features_gui.windows']

package_data = \
{'': ['*'], 'sport_activities_features_gui': ['media/*']}

install_requires = \
['PyQt5>=5.15.7,<6.0.0',
 'PyQt6>=6.5.1,<7.0.0',
 'QtAwesome>=1.2.1,<2.0.0',
 'sip>=6.7.9,<7.0.0',
 'sport-activities-features>=0.3.7,<0.4.0']

setup_kwargs = {
    'name': 'sport-activities-features-gui',
    'version': '0.2.0',
    'description': 'GUI for sport-activities-features package',
    'long_description': None,
    'author': 'otiv33',
    'author_email': 'vito.abeln@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

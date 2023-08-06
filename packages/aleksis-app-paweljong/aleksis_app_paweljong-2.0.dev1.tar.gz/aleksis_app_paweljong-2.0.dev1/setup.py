# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.paweljong',
 'aleksis.apps.paweljong.migrations',
 'aleksis.apps.paweljong.templatetags']

package_data = \
{'': ['*'],
 'aleksis.apps.paweljong': ['frontend/*',
                            'frontend/messages/*',
                            'locale/*',
                            'locale/ar/LC_MESSAGES/*',
                            'locale/de_DE/LC_MESSAGES/*',
                            'locale/fr/LC_MESSAGES/*',
                            'locale/la/LC_MESSAGES/*',
                            'locale/nb_NO/LC_MESSAGES/*',
                            'locale/tr_TR/LC_MESSAGES/*',
                            'static/css/*',
                            'static/js/paweljong/*',
                            'templates/paweljong/*',
                            'templates/paweljong/event/*',
                            'templates/paweljong/event_registration/*',
                            'templates/paweljong/info_mailing/*',
                            'templates/paweljong/print/*',
                            'templates/paweljong/registration_state/*',
                            'templates/paweljong/term/*',
                            'templates/paweljong/voucher/*',
                            'templates/templated_email/*']}

install_requires = \
['aleksis-app-postbuero==2.0.1.dev0',
 'aleksis-app-tezor==2.0dev1',
 'aleksis-core>=3.0b0,<4.0',
 'django-formtools==2.3',
 'django-localflavor>=3.0,<4.0',
 'django-starfield>=1.0,<2.0']

entry_points = \
{'aleksis.app': ['paweljong = aleksis.apps.paweljong.apps:DefaultConfig']}

setup_kwargs = {
    'name': 'aleksis-app-paweljong',
    'version': '2.0.dev1',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp Paweljong (Camp/Event management)',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp Paweljong (Camp/Event management)\n==================================================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS®`_ platform.\n\nFeatures\n--------\n\nThe author of this app did not describe it yet.\n\nLicence\n-------\n\n::\n\n  Copyright © 2018, 2021, 2022 Dominik George <dominik.george@teckids.org>\n  Copyright © 2019, 2022 Tom Teichler <tom.teichler@teckids.org>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\nTrademark\n---------\n\nAlekSIS® is a registered trademark of the AlekSIS open source project, represented\nby Teckids e.V. Please refer to the `trademark policy`_ for hints on using the trademark\nAlekSIS®.\n\n.. _AlekSIS®: https://edugit.org/AlekSIS/AlekSIS\n.. _European Union Public Licence: https://eupl.eu/\n.. _trademark policy: https://aleksis.org/pages/about\n',
    'author': 'Tom Teichler',
    'author_email': 'tom.teichler@teckids.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hacknfun.camp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

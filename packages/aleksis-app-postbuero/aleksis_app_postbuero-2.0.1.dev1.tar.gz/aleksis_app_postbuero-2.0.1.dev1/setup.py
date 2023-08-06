# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.postbuero',
 'aleksis.apps.postbuero.migrations',
 'aleksis.apps.postbuero.util']

package_data = \
{'': ['*'],
 'aleksis.apps.postbuero': ['frontend/*',
                            'frontend/components/mail_addresses/*',
                            'frontend/components/mail_domains/*',
                            'frontend/messages/*',
                            'static/*',
                            'templates/templated_email/*']}

install_requires = \
['AlekSIS-Core>=3.0b0,<4.0']

entry_points = \
{'aleksis.app': ['postbuero = aleksis.apps.postbuero.apps:PostBueroConfig']}

setup_kwargs = {
    'name': 'aleksis-app-postbuero',
    'version': '2.0.1.dev1',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp Postbuero (Mail server management)',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp Postbuero (Mail server management)\n============================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS®`_ platform.\n\nFeatures\n--------\n\nPostbuero provides integration with various mail server functionality, among which are:\n\n * Management of supported mail domains\n * Management of mail addresses (mailboxes) for persons\n\n   * Public registration for domains allowing it\n\n * Management of mail addresses (aliases) for groups\n\n   * Including support for members, owners, and guardians\n\n * `WebMilter`_ support for Postfix\n\n   * Alias resolution for persons and groups\n\nLicence\n-------\n\n::\n\n  Copyright © 2020 Tom Teichler <tom.teichler@teckids.org>\n  Copyright © 2022 Tom Teichler <tom.teichler@teckids.org>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\nTrademark\n---------\n\nAlekSIS® is a registered trademark of the AlekSIS open source project, represented\nby Teckids e.V. Please refer to the `trademark policy`_ for hints on using the trademark\nAlekSIS®.\n\n.. _AlekSIS®: https://edugit.org/AlekSIS/official/AlekSIS\n.. _WebMilter: https://docs.bergblau.io/concepts/webmilter/\n.. _European Union Public Licence: https://eupl.eu/\n.. _trademark policy: https://aleksis.org/pages/about\n',
    'author': 'Tom Teichler',
    'author_email': 'tom.teichler@teckids.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://aleksis.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

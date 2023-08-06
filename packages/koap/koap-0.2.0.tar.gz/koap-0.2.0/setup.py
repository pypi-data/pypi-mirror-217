# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koap', 'koap.facade', 'koap.facade.epa', 'koap.facade.vsdm']

package_data = \
{'': ['*'],
 'koap': ['api-telematik/*',
          'api-telematik/cm/cc/*',
          'api-telematik/cm/common/*',
          'api-telematik/cm/uf/*',
          'api-telematik/conn/*',
          'api-telematik/conn/amtss/*',
          'api-telematik/conn/nfds/*',
          'api-telematik/conn/phrs/*',
          'api-telematik/conn/tbauth/*',
          'api-telematik/conn/vsds/*',
          'api-telematik/consumer/*',
          'api-telematik/ext/*',
          'api-telematik/ext/HL7V3/NE2008/coreschemas/*',
          'api-telematik/ext/HL7V3/NE2008/multicacheschemas/*',
          'api-telematik/ext/IHE/*',
          'api-telematik/ext/ebRS/*',
          'api-telematik/fa/amtss/*',
          'api-telematik/fa/nfds/*',
          'api-telematik/fa/nfds/common/*',
          'api-telematik/fa/vsds/*',
          'api-telematik/fd/phr/*',
          'api-telematik/images/*',
          'api-telematik/ksr/*',
          'api-telematik/stoerungsampel/*',
          'api-telematik/tel/error/*',
          'api-telematik/tel/version/*',
          'api-telematik/vpnzugd/*',
          'api-telematik/vzd/*']}

install_requires = \
['jwcrypto>=1.5.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyopenssl>=23.2.0,<24.0.0',
 'requests-pkcs12>=1.18,<2.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'xmltodict>=0.13.0,<0.14.0',
 'zeep>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'koap',
    'version': '0.2.0',
    'description': '',
    'long_description': "# KOAP: Modern Konnektor SOAP Library\n\n## Configuration using environment variables\n\n| Environment variable | Comment |\n| --- | --- |\n| `KONNEKTOR_BASE_URL` | Base URL for Konnektor. The `connector.sds` must be available at `{KONNEKTOR_BASE_URL}/connector.sds`|\n| `KONNEKTOR_MANDANT_ID` | Context Mandant ID (Tenant)|\n| `KONNEKTOR_CLIENT_SYSTEM_ID` | Context Client System ID|\n| `KONNEKTOR_WORKPLACE_ID` | Context Workplace ID|\n| `KONNEKTOR_USER_ID` | Context UserID (optional)|\n| *Basic Auth* |\n| `KONNEKTOR_AUTH_BASIC_USERNAME` | Username for Basic authentication| \n| `KONNEKTOR_AUTH_BASIC_PASSWORD`| Password for Basic authentication| \n| *Mutual TLS Auth* |\n| Not implemented yet | \n\n```bash\nexport KONNEKTOR_BASE_URL=https://.../\nexport KONNEKTOR_MANDANT_ID=m1\nexport KONNEKTOR_CLIENT_SYSTEM_ID=c1\nexport KONNEKTOR_WORKPLACE_ID=w1\nexport KONNEKTOR_USER_ID=user1\nexport KONNEKTOR_AUTH_BASIC_USERNAME=user1\nexport KONNEKTOR_AUTH_BASIC_PASSWORD='use strong passwords in production'\n```\n\nOnce the environmant variables are set, the `koap.config.ConnectorConfig`can be instantiated without parameters. We make use of [Pydantic Model Config](https://docs.pydantic.dev/latest/usage/model_config/).\n\n```python\nfrom koap.config import ConnectorConfig\nfrom koap.client import ConnectorClient\n\nconfig = ConnectorConfig()\n\nclient = ConnectorClient(config)\n\nevent_service = client.create_service_client('EventService', '7.2.0')\n\ncards = event_service.GetCards(client.context())\n\nprint(cards)\n\n```\n\n## Configuration in code\n\n```python\nfrom koap.config import ConnectorConfig\nfrom koap.client import ConnectorClient\n\nconfig = ConnectorConfig(\n    base_url='https://.../',\n    mandant_id='m1',\n    client_system_id='c1',\n    workplace_id='w1',\n    user_id='user1',\n    # Basic Auth\n    auth_basic_username='user1',\n    auth_basic_password='use secure passwords in production',\n)\n\nclient = ConnectorClient(config)\n\nevent_service = client.create_service_client('EventService', '7.2.0')\n\ncards = event_service.GetCards(client.context())\n\nprint(cards)\n```\n\n## Development\n\n```bash\ngit submodule init\ngit submodule update\npoetry install\n```\n\n",
    'author': 'Sergej Suskov',
    'author_email': 'git@spilikin.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

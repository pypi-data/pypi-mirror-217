# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylibsdm',
 'pylibsdm.backend',
 'pylibsdm.cli',
 'pylibsdm.tag',
 'pylibsdm.tag.ntag424dna']

package_data = \
{'': ['*']}

install_requires = \
['nfcpy>=1.0.4,<2.0.0',
 'pycryptodome>=3.18.0,<4.0.0',
 'pydantic>=1.10.9,<2.0.0']

extras_require = \
{'cli': ['typer[all]>=0.9.0,<0.10.0']}

entry_points = \
{'console_scripts': ['sdmutil = pylibsdm.cli:app'],
 'pylibsdm.tags': ['ntag424dna = pylibsdm.tag.ntag424dna:Tag']}

setup_kwargs = {
    'name': 'pylibsdm',
    'version': '1.0.0a0.dev0',
    'description': 'Python library for handling Secure Dynamic Messaging (SDM) of NFC cards like the NTAG 424 DNA',
    'long_description': '<!--\nSPDX-FileCopyrightText: © 2023 Dominik George <nik@velocitux.com>\n\nSPDX-License-Identifier: LGPL-2.0-or-later\n-->\n\n# pylibsdm - NFC Secure Dynamic Messaging with Python\n\npylibsdm is a Python library (SDK) for handling Secure Dynamic Messaging (SDM)\nof NFC cards with Python.\n\nSecure Dynamic Messaging is a technology that adds security features to\nNFC tags using standard mechanisms. While standard NFC data (so-called\nNDEF messages, e.g. texts, URLs, etc.) can be written to any compatible\ntag, SUN-capable tags can cryptographically sign and optionally also\nencrypt parts of the data, which can then still be read by any standard\nNFC reader.\n\n## Features\n\n* Card management / configuration\n  * Configuration of NDEF file settings (mirrors, offsets, used keys,…)\n  * Configuration of NDEF file data (URL)\n  * Provisioning of keys\n* Backend implementation for SUN (Secure Unique NFC)\n  * Decryption and validation of SDM data (mirrors)\n  * Validation of information from URI parameters\n\n## Supported tags\n\n* [NTAG 424 DNA](https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-and-labels/ntag-424-dna-424-dna-tagtamper-advanced-security-and-privacy-for-trusted-iot-applications:NTAG424DNA)\n  ([specification](https://www.nxp.com/docs/en/application-note/AN12196.pdf))\n\n## Installation and usage\n\n`pylibsdm` is shipped as a standard Python library and cann be installed\nfrom PyPI:\n\n```sh\npip install "pylibsdm[cli]"\n```\n\nThe `cli` extra installs the `sdmutil` command-line utility, which can\nbe used as a stand-alone tool to handle tags.\n\n### Usage as a library in own code\n\nThe following examples show how to use `pylibsdm` within custom\napplications. It can, as such, be seen as an SDK for writing SUN-capable\napplications.\n\n#### Configuring a tag in code\n\nWe will configure a tag for the following behaviour:\n\n * Change app keys 1 and 2 to our own keys\n * Configure write access to NDEF data to need authentication with app key 1\n * Configure SDM to encrypt and sign data with key 2\n * Mirror encrypted PICC data (UID and read counter)\n * Mirror a CMAC for validation\n\n```python\nfrom pylibsdm.tag.ntag424dna import Tag\n\n# We need a working tag object from nfcpy\nnfc_tag = ...\n\n# Configure the SDM tag object for communication\nsdm_tag = Tag(nfc_tag)\n\n# Set current master app key nr 0 for authentication\nsdm_tag.set_key(0, b"\\x00\\x11\\x22\\x33\\x44\\x55\\x66\\x77\\x88\\x99\\xaa\\xbb\\xcc\\xdd\\xee\\xff")\n\n# Change app keys 1 and 2 for later use\nsdm_tag.change_key(1, 16 * b"\\xaa")\nsdm_tag.change_key(2, 16 * b"\\xaa")\n\n# Configure attributes for mirroring\nfile_option = FileOption(sdm_enabled=True, comm_mode=CommMode.PLAIN)\nsdm_options = SDMOptions(\n    uid=True,\n    read_ctr=True,\n    read_ctr_limit=False,\n    enc_file_data=False,\n    tt_status=False,\n    ascii_encoding=True,\n)\n\n# We configure free reading access of NDEF, writing data is limited to app key 1,\n#  and changing file settings to the master app key 0\naccess_rights = AccessRights(\n    read=AccessCondition.FREE_ACCESS,\n    write=AccessCondition.1,\n    read_write=AccessCondition.KEY_1,\n    change=AccessCondition.KEY_0,\n)\n# When reading the NDEF message, app key 2 is used for\nsdm_acceess_rights = SDMAccessRights(\n    file_read=AccessCondition.KEY_2,\n    meta_read=AccessCondition.KEY_2,\n    ctr_ret=AccessCondition.KEY_2,\n)\n\n# Aggregate options and offsets in NDEF data\nfile_settings = FileSettings(\n    file_option=file_option,\n    access_rights=access_rights,\n    sdm_options=sdm_options,\n    sdm_access_rights=sdm_acceess_rights,\n    picc_data_offset=32,\n    mac_offset=67,\n    mac_input_offset=67,\n)\nsdm_tag.change_file_settings(2, file_settings)\n```\n',
    'author': 'Dominik George',
    'author_email': 'nik@naturalnet.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/Bergblau/pylibsdm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

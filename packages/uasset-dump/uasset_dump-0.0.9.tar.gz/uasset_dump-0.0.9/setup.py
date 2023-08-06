# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bootloader',
 'bootloader.ue',
 'bootloader.ue.cli',
 'bootloader.ue.constant',
 'bootloader.ue.model',
 'bootloader.ue.utils']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19.3,<2.0.0']

entry_points = \
{'console_scripts': ['ueprjver = bootloader.ue.cli.uassetdump:run']}

setup_kwargs = {
    'name': 'uasset-dump',
    'version': '0.0.9',
    'description': 'Command-line Interface (CLI) responsible for returning the list of the assets of an Unreal Engine project into a JSON structure',
    'long_description': '# Unreal Engine Assets Dump\n\nCommand-line Interface (CLI) responsible for returning the list of the assets of an Unreal Engine project into a JSON structure.\n\n## Development\n\n### Poetry\n\n_Unreal Engine Assets Dump_ project used Poetry to declare all its dependencies.  [Poetry](https://python-poetry.org/) is a python dependency management tool to manage dependencies, packages, and libraries in your python project.\n\nWe need to create the Python virtual environment using Poetry:\n\n```shell\npoetry env use /Users/Shared/Epic\\ Games/UE_5.2/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3\n```\n\nWe can enter this virtual environment and install all the required dependencies:\n\n```shell\npoetry shell\npoetry update\n```\n\n\n## Publication\n\nTo publish a new version of the _Unreal Engine Assets Dump_ library to [Pypi](https://pypi.org/), we need to execute the following command:\n\n```shell\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n```\n\nWhere the environment variables:\n\n- `$PYPI_USERNAME`: The value `__token__`\n- `$PYPI_PASSWORD`: The [API token](https://pypi.org/manage/account/token/) used to authenticate when uploading packages to PyPI (e.g., `pypi-...`)\n\nWe generally defined a `.env` file and add these environment variables:\n\n```text\n# Copyright (C) 2023 Bootloader.  All rights reserved.\n#\n# This software is the confidential and proprietary information of\n# Bootloader or one of its subsidiaries.  You shall not disclose this\n# confidential information and shall use it only in accordance with the\n# terms of the license agreement or other applicable agreement you\n# entered into with Bootloader.\n#\n# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE\n# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT\n# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR\n# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE\n# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF\n# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.\n\n# The Python Package Index (PyPI) API token to authenticate when\n# uploading this package to PyPI.\nPYPI_USERNAME=__token__\nPYPI_PASSWORD=pypi-(...)\n```\n\n\n## Installation\n\nTo install _Unreal Engine Assets Dump_ library to Unreal Engine, execute the following command.\n\n```shell\n/Users/Shared/Epic\\ Games/UE_5.1/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3 -m pip install --upgrade uasset-dump\n/Users/Shared/Epic\\ Games/UE_5.2/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3 -m pip install --upgrade uasset-dump\n```\n\n/Users/admin/Library/JenkinsAgent/workspace/client-app/scooby-app-build/main/Scooby/Content\n\n## Execution\n\nThen we can load our Unreal Engine project in Unreal Engine Editor and execute the following Python instructions in the Output Log drawer:\n\n```shell\nfrom bootloader.ue.utils import uasset_dump\nuasset_dump.dump_assets(\'/Users/dcaune/Devel/Bootloader/bootloader-human-trainer-ar5/Content\')\n```\n\nThis prints long JSON data.  For instance:\n\n```json\n[\n  {\n    "asset_name": "A_d2_ChangeOutfit_01",\n    "asset_class_path": "/Script/Engine/AnimSequence",\n    "package_name": "/Game/ArtAssets/Pets/QuadrupedDog/Animations/A_d2_ChangeOutfit_01",\n    "dependencies": [\n      "/Game/ArtAssets/Pets/QuadrupedDog/Mesh/S_d2"\n    ]\n  },\n  {\n    "asset_name": "A_d2_ChangeOutfit_02",\n    "asset_class_path": "/Script/Engine/AnimSequence",\n    "package_name": "/Game/ArtAssets/Pets/QuadrupedDog/Animations/A_d2_ChangeOutfit_02",\n    "dependencies": [\n      "/Game/ArtAssets/Pets/QuadrupedDog/Mesh/S_d2"\n    ]\n  },\n  (...)\n]\n```\n\n```shell\nexport UNREAL_ENGINE_PROJECT_PATH=/Users/admin/Library/JenkinsAgent/workspace/client-app/scooby-app-build/main/Scooby/Scooby.uproject\n\nexport UNREAL_ENGINE_ASSET_DUMP_FILE_PATH=/Users/admin/bootloader-scooby-uassets.dump.json\n\n"`find "/Users/Shared/Epic Games/UE_5.2" -name UnrealEditor-Cmd`" \\\n    "$UNREAL_ENGINE_PROJECT_PATH" \\\n    -run=pythonscript \\\n    -stdout \\\n    -Unattended \\\n    -script="/Users/admin/Downloads/run.py"\n\necho $?;\n```\n\n# Command Line Execution\n\n```shell\n\n\n```',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel@bootloader.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bootloader-studio/cli-uasset-dump',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

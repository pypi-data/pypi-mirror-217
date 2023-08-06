# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdss', 'mdss.scenarios']

package_data = \
{'': ['*']}

install_requires = \
['MDAnalysis==2.1.0',
 'dictances==1.5.3',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pytest-mock>=3.10.0,<4.0.0',
 'pytest>=7.2.0,<8.0.0',
 'scikit-learn>=1.2.2,<2.0.0']

entry_points = \
{'console_scripts': ['mdss = mdss.run:run',
                     'mdss_scenario_1 = mdss.scenarios.scenario_1:run',
                     'mdss_scenario_2 = mdss.scenarios.scenario_2:run',
                     'mdss_scenario_3 = mdss.scenarios.scenario_3:run']}

setup_kwargs = {
    'name': 'mdsubsampler',
    'version': '0.0.2',
    'description': '',
    'long_description': '# MDSubSampler: Molecular Dynamics SubSampler\n\n[![PyPI version](https://badge.fury.io/py/mdsubsampler.svg)](https://badge.fury.io/py/mdsubsampler)\n\nMDSubSampler is a Python library and toolkit for a posteriori subsampling of multiple trajectory data for further analysis. This toolkit implements uniform, random, stratified sampling, bootstrapping and targeted sampling to preserve the original distribution of relevant geometrical properties.\n\n## Prerequisites\n\nThis project requires Python (version 3.9.1 or later). To make sure you have the right version available on your machine, try running the following command. \n\n```sh\n$ python --version\nPython 3.9.1\n```\n\n## Table of contents\n\n- [Project Name](#project-name)\n  - [Prerequisites](#prerequisites)\n  - [Table of contents](#table-of-contents)\n  - [Getting Started](#getting-started)\n  - [Installation](#installation)\n  - [Usage](#usage)\n    - [Workflow](#workflow)\n    - [Scenarios](#scenarios)\n    - [Parser](#parser)\n    - [Development](#development)\n  - [Authors](#authors)\n  - [License](#license)\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for analysis and development purposes. \n\n## Installation\n\n**BEFORE YOU INSTALL:** please read the [prerequisites](#prerequisites)\n\nTo install and set up the library, run:\n\n```sh\npip install MDSubSampler\n```\n\n## Usage \n\n### Workflow\n\nInput:\n- Molecular Dynamics trajectory \n- Geometric property\n- Atom selection [optional - default is "name CA"]\n- Reference structure [optional] \n- Sample size or range of sizes\n- Dissimilarity measure [optional - default is "Bhattacharyya"]\n\nOutput:\n- .dat file with calculated property for full trajectory (user input)\n- .dat file(s) with calculated property for one or all sample sizes input\n- .xtc file(s) with sample trajectory for one or all sample sizes\n- .npy file(s) with sample trajectory for one or all sample sizes \n- .npy training set for ML purposes for sample trajectory (optional)\n- .npy testing set for ML purposes for sample trajectory (optional)\n- .npy file(s) with sample trajectory for one or for all sample sizes \n- .png file with overlapped property distribution of reference and sample\n- .json file report with important statistics from the analysis\n- .txt log file with essential analysis steps and information\n\n### Scenarios\n\nTo run scenarios 1,2 or 3 you can download your protein trajectory and topology file (.xtc and .gro files) to the data folder and then run the following:\n\n```sh\npython mdss/scenarios/scenario_1.py data/<YourTrajectoryFile>.xtc data/<YourTopologyfile>.gro <YourPrefix>\n```\nScenarios 1,2 and 3 are also available in Jupyter Notebooks format, can be used as templates and can be modified interactively according to the user\'s needs. You can also find more advanced scenarios in the cookbook directory. If you clone the library locally to your machine, then run the following command before you run the cells.  \n\n```sh\n%cd <pathToMDSubSamplerDirectory>\n```\n\n### Parser\n\nIf you are a terminal lover you can use the terminal to run the code and make a choice for the parser arguments. To see all options and choices run:\n\n```sh\npython mdss/run.py --help\n```\nOnce you have made a selection of arguments, your command can look like the following example:\n\n```sh\npython mdss/run.py \\\n  --traj "data/<YourTrajectoryFile>.xtc" \\\n  --top "data/<YourTopologyFile>.gro" \\\n  --prefix "<YourPrefix>" \\\n  --output-folder "data/<YourResultsFolder>" \\\n  --property=\'DistanceBetweenAtoms\' \\\n  --atom-selection=\'G55,P127\' \\\n  --sampler=\'BootstrappingSampler\' \\\n  --n-iterations=50 \\\n  --size=<SampleSize> \\\n  --dissimilarity=\'Bhattacharyya\'\n```\n\n### Development\n\n#### With Poetry\n\nStart by either downloading the tarball file from https://github.com/alepandini/MDSubSampler to your local machine or cloning this repo on your local machine:\n\n```sh\ngit clone git@github.com:alepandini/MDSubSampler.git\ncd MDSubSampler\n```\n\nFollowing that, download and install poetry from https://python-poetry.org/docs/#installation\n\n\nFinally, run the following:\n\n```sh\npoetry install\npoetry build\npoetry shell\n```\nYou can now start developing the library.\n\n#### With Docker\n\nStart by installing Docker using this link https://docs.docker.com/get-docker/.\n\nInitially a Docker image will need to be built. To do this run the following command:\n\n```sh\ndocker build -t <image name> .\n```\n\nThen run the following command to get access to a shell with all dependencies installed:\n\n```sh\ndocker run -it -v $(pwd):/app -e PYTHONPATH=/app <image name> /bin/bash\n```\n\nThis will also mirror the local filesystem in the Docker image, so that any local change will\nbe reflected in the running container, and vice-versa, using a Docker volume.\n\nThe repo also includes two handy scripts to run all of the above faster (an image called\n`subsampler` will be created):\n\n```sh\n./build-docker\n./run-docker\n```\n\nAfter dropping in the Docker shell, all dependencies will be installed, and the package scripts\nwill also be in scope (the `mdss` command and all scenarios declared in `pyproject.toml`).\n\n### Authors\n\n* **Namir Oues** - [namiroues](https://github.com/namiroues)\n* **Alessandro Pandini** [alepandini](https://github.com/alepandini)\n\n### License\n\nThe library is licensed by **GPL-3.0**\n',
    'author': 'Namir Oues',
    'author_email': 'namir.oues@brunel.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

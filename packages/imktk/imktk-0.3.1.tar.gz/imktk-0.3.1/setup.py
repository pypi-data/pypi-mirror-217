# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imktk', 'imktk.constants', 'imktk.dataarray_methods', 'imktk.dataset_methods']

package_data = \
{'': ['*']}

install_requires = \
['netCDF4>=1.5.8,<2.0.0',
 'pandas<2',
 'scipy>=1.9.0,<2.0.0',
 'xarray>=0.20.1,<0.21.0']

entry_points = \
{'console_scripts': ['imktk = imktk:main']}

setup_kwargs = {
    'name': 'imktk',
    'version': '0.3.1',
    'description': 'Toolkit provided by IMK at KIT',
    'long_description': '# IMK Toolkit\n\nThis toolkit provides [post-processing scripts](/imktk) developed by members of the\n[Institute of Meteorology and Climate Research (IMK)](https://dev.to/epassaro/keep-your-research-reproducible-with-conda-pack-and-github-actions-339n)\nat the Karlsruhe Institute of Technology (KIT). The goal of this module is to\ngather together python post-processing scripts for the analysis of netCDF data\nand distribute them easily.\n\n## Usage\nSimply import the library using `import imktk`. From then on all scripts are\navailable using the `imktk` attribute:\n\n```python\nimport imktk\n\nds = imktk.tutorial.open_dataset("toy_weather")  # Load example dataset\nanomaly_free_tmin = ds.tmin.imktk.anomalies()  # Select dataarray `xr.tmin` and execute anomalies script\n```\n\nThe following is a list of available scripts:\n\n\n| Description | Example usage | Link to Script\n|--------|--------|-------------|\n|Calculate temperature for adiabatic process in air|`ds.tmin.imktk.ad_temp(temp_at_0, press_at_0)`| [here](./imktk/dataarray_methods/ad_temp.py)|\n|Calculate monthly anomalies|`ds.tmin.imktk.anomalies()`| [here](./imktk/dataarray_methods/anomalies.py)|\n|Calculate monthly climatology|`ds.tmin.imktk.climatology()`| [here](./imktk/dataarray_methods/climatology.py)|\n|Interpolation routine for flight track (incl. aircraft and satellites)| `ds.tmin.imktk.flight_track(**dims)` | [here](./imktk/dataarray_methods/flight_track.py) |\n|Calculate number density from mixing ratio, temperature and pressure| `ds.tmin.imktk.num_den(temp, press)` | [here](./imktk/dataarray_methods/num_den.py)|\n|Calculate saturation vapour pressure over ice for temperatures > 110 K| `ds.tmin.imktk.vapour_pres_ice()` | [here](./imktk/dataarray_methods/vapour_pres_ice.py)|\n|Calculate saturation vapour pressure over liquid water for temperatures 123 K < T < 332 K|`ds.tmin.imktk.vapour_pres_liq()` | [here](./imktk/dataarray_methods/vapour_pres_liq.py)|\n\n## Getting Started\n\nThe easiest method to test the module is to use an interactive session with docker.\nIn this environment you will have a Python 3 environment with all necessary dependencies already installed.\n\n```bash\ndocker run -it imktk/imktk:latest bash\n```\n\n> For the brave: You can test the latest release candidate by changing `latest` to `testing`\n\n## Install\n\nChoose one of the following methods to install the package:\n\n1. Install using `pip`\n2. Install using `conda`\n3. Install using `git clone`\n\n> This package supports only Python 3 with version `>=3.7`. If you are using\n> an earlier version of Python please consider updating.\n\n### `pip`\n\nReleases are automatically uploaded to PyPI. Please execute following command\nto install the package.\n\n```bash\npython3 -m pip install imktk\n```\n\n### `conda`\n\nCurrently the package does no support native installation using `conda`\nrespectively `conda-forge`. This feature is on the roadmap and you can follow\nits process using issue [#34](https://github.com/imk-toolkit/imk-toolkit/issues/34).\nThe current workaround for `conda` installation is to use the following steps\nfor any given environment `<env>`.\n\n1. Activate the environment\n\n    ```bash\n    conda activate <env>\n    ```\n\n2. Install using `pip`\n\n    ```bash\n    python3 -m pip install imktk\n    ```\n\n### `git clone`\n\nIt is also possible to install the package natively by cloning the repository.\nIf you are interested in using this method of installation please follow\nthese steps\n\n1. Install build dependencies\n\n    ```bash\n    python3 -m pip install build\n    ```\n\n2. Clone repository\n\n    ```bash\n    git clone https://github.com/imk-toolkit/imk-toolkit.git\n    ```\n\n3. Generate the Python packages\n\n    ```bash\n    python3 -m build  # or `make build`\n    ```\n\n4. Install packages\n\n    ```bash\n    pip3 install dist/imktk-<current.version>-py3-none-any.whl  # or `make install`\n    ```\n\n> Please be aware that this package uses `HDF5` and `netCDF` c-libraries in the\n> backend. If you are installing using `git clone` the `HDF5_DIR` environment\n> variable with the location of the HDF5 header files needs to be set.\n\n## Further reading\n\nIf you are interested in the inner workings of the package and details of the\nimplementation please refer to the embedded [README.md](/imktk/README.md).\n',
    'author': 'Uğur Çayoğlu',
    'author_email': 'Ugur.Cayoglu@kit.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/imk-toolkit/imk-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

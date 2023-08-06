# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pySPM', 'pySPM.tools', 'pySPM.utils']

package_data = \
{'': ['*'], 'pySPM': ['data/*']}

install_requires = \
['ipython>=8.12.0,<9.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pywavelets>=1.4.1,<2.0.0',
 'scikit-image>=0.20.0,<0.21.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'pyspm',
    'version': '0.3.2',
    'description': 'Library to handle SPM and ToF-SIMS data',
    'long_description': '[![Downloads](https://pepy.tech/badge/pyspm)](https://pepy.tech/project/pyspm)\n[![PyPi version](https://img.shields.io/pypi/v/pySPM)](https://pypi.python.org/pypi/pySPM/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.998575.svg)](https://doi.org/10.5281/zenodo.998575)\n\n# pySPM\n\npySPM is a Python library in order to read, handle and plot Scanning Probe Microscopy (SPM) images as well as ToF-SIMS\ndata.\n\nSupported SPM file formats:\n\n* Nanoscan .xml file format\n* Bruker\n* Iontof ToF-SIMS fileformats:\n    * ITA\n    * ITM\n    * ITS\n* Nanonis SXM file\n\n## Important\n\nThis library is offered as it is and is still in development. Please note that reading the raw data was done by reverse\nengineering and guessing and not with a manual as the file format is proprietary. It seems to work well with the data\nused by the developer of this library, but there is **NO GUARANTEE** that this library will work correctly with your own\nspecific data.\n\nIf you find bugs and issues, please report them to the developer: https://github.com/scholi/pySPM/issues\n\n## Installation\n\n### From PyPI\n\n```bash\npip install pySPM\n```\n### From GitHub\n\n#### With poetry\n\n```bash\npoetry add git+https://github.com/scholi/pySPM.git\n```\n\n#### With pip\n\n```bash\npip install git+https://github.com/scholi/pySPM.git\n```\n\n### Optional dependencies\n\n`PyQT5` for GUI controls.\n\n## Documentation\n\nThe documentation is still in its early stage\n[read the documentation](https://nbviewer.jupyter.org/github/scholi/pySPM/blob/master/doc/pySPM%20Documentation.ipynb)\n\nThere is also\na [short introduction to pySPM for ToF-SIMS data](https://nbviewer.jupyter.org/github/scholi/pySPM/blob/master/doc/Introduction%20to%20pySPM%20for%20ToF-SIMS%20data.ipynb)\n\n## Citing\n\nIf you use this library for your work, please think about citing it.\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.998575.svg)](https://doi.org/10.5281/zenodo.998575)\n\nOlivier Scholder. (2018, November 28). scholi/pySPM: pySPM v0.2.16 (Version v0.2.16).\nZenodo. http://doi.org/10.5281/zenodo.998575\n\n## News\n\n### ITA files are writable\n\nFrom now on you can, not only view the ita files, but you can also write them by supplying the parameter\n_readable=False_ to _pySPM.ITA_ or _pySPM.ITM_. For the moment this is still a non-user-friendly procedure, but you can\nedit each ITStr Block with the ```edit_block()``` function. Be careful, because if the new data has a different size\nthan the old one, a new block is created, but the old one is also kept. This means that your ITA file size will grow.\nYou can also add new channels and images with the more user-friendly function ```pySPM.ITA.add_new_images()```.\n:warning: It is highly advised to copy the ita file before making any change. You can use the following code to copy the\nita in a temporary ita before making any change.\n\n```python\nfrom shutil import copyfile\nimport pySPM\n\nfilename = "scanfile.ita"\ncopyfile(src=filename, dst="temp.ita")\nA = pySPM.ITA("temp.ita", readonly=False)\n```\n\n### New tools\n\nThe library comes with three scripts to make your life easier. Those scripts are located in your python folder in the\nScripts directory. You can also run them from the command line.\n\n#### stability\n\nAllows you to select a measurement folder and display the Emission Current and Suppressor voltage in function of the\ntime/scan number.\nThis allows you to verify the stability of your source during your measurements.\n![stability_screenshot](doc/images/Capture_stability.png)\n\nsee the [wiki](../../wiki/stability) for more info\n\n#### plotter\n\nAllows you to plot the parameter logged by your logfile. If SurfaceLab is running this script will detect which logfile\nis beeing saved and will display the values live (the plot is refreshed every 3s in order add the new data). You can\nalso provide as first argument the logfile path (or in windows you can drag&drop the logfile over the plotter app).\n![plotter_screenshot](doc/images/Capture_plotter.png)\n\nsee the [wiki](../../wiki/plotter) for more info\n\n#### timer\n\nIf you are using SurfaceLab, this app will display a small progressbar of your measurement and will calculate the\nremaining time in function of the elapsed time, the total number of scans and the elapsed number of scan.\n![timer_screenshot](doc/images/Capture_timer.png)\n\nsee the [wiki](../../wiki/timer) for more info\n\n#### spectra\n\nThis tool can display spectra, visualize rapidly peaks assignment and perform fast mass calibration.\nYou can give an ITA filename as argument or if none a GUI filedialog will ask you for one. You will then see your\nspectrum.\nYou can navigate with the scroll of the mouse to zoom in & out. You can use the keyboard <kbd>+</kbd> and <kbd>-</kbd>\nto shift your spectra by ±1 Dalton. You can use left-mouse-button and drag to shift your spectra. You can perform very\nquick mass calibration by Right-Mouse-Click on one measurement peak (hold the mouse) the move to the element mark you\nwant to assign your peak and release the mouse. The mass calibration values should then be updated on the left table and\nthe mass calibration performed live so that you can see immediately the changes.\n![spectra_screenshot](doc/images/Capture_spectra.png)\n\nsee the [wiki](../../wiki/spectra) for more info\n',
    'author': 'Olivier Scholder',
    'author_email': 'o.scholder@gmail.com',
    'maintainer': 'Dinesh Pinto',
    'maintainer_email': 'annual.fallout_0z@icloud.com',
    'url': 'https://github.com/scholi/pySPM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

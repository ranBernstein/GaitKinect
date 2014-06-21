from distutils.core import setup
import matplotlib

import sys
sys.path.append("C:\Users\\ran\git\Master\Fourier\utils")
print sys.path[-1]

import utils
import py2exe
matplotlib.use("Qt4Agg")

from scipy.sparse.csgraph import _validation
opts =  { 'py2exe': { 'includes': ['scipy.sparse.csgraph._validation'] }}
setup(console=['skeletonGUI.py'],
    options = opts
)
"""
# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3)
from distutils.core import setup
import py2exe
import matplotlib
# We need to import the glob module to search for all files.
import glob


# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
matplotlib.use("Qt4Agg")
data_files=matplotlib.get_py2exe_datafiles()
opts = {
    'py2exe': { "includes" : ["utils"], 
               'packages' : ['utils','utils.kinect']
              }
       }
# for console program use 'console = [{"script" : "skeletonGUI.py"}]
setup(console=[{"script" : "skeletonGUI.py"}], options=opts, data_files=data_files)
"""
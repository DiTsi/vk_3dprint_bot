
# from volume import stl_volume, stl_mass

# DENSITY = 1.05 # g/cm^3

import time
import ntpath
from os import rename, path
import re

filepath = <path/file.ong>
newfilepath = <filepath>

def mv_file(filepath, folder):
    date = time.strftime('%y%m%d_%H%M%S__', time.localtime(path.getmtime(filepath)))
    basename = ntpath.basename(filepath)
    # print(date + basename)
    # print()
    rename(filepath,  folder + "/" + date + basename)

mv_file(filepath, newfilepath)


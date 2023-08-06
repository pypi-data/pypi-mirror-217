import os
import sys
import inspect


# Adds /serial to the path.
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) +
                              "//connection_specific//serial")
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
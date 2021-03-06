"""
Unittests for examples.
All examples are executed to check against latest code base.
"""
from __future__ import print_function, division
import unittest

import os
import imp

# ----------------------------------------------------------------
# List of python files to test
# ----------------------------------------------------------------
def _pyFilesInFolder(dir):
    from os import walk
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend([os.path.join(dirpath, name) for name in filenames])
    return [f for f in files if f.endswith('.py')]


examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'examples')
notebookdir = os.path.join(examples_dir, 'notebooks-py')
tedir = os.path.join(examples_dir, 'tellurium-files')
py_files = []
py_files.extend(_pyFilesInFolder(notebookdir))
py_files.extend(_pyFilesInFolder(tedir))

# ----------------------------------------------------------------
# Test class
# ----------------------------------------------------------------
class PythonExampleTestCase(unittest.TestCase):

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        import matplotlib
        matplotlib.pyplot.switch_backend("Agg")

# ----------------------------------------------------------------
# Dynamic generation of tests from python files
# ----------------------------------------------------------------
def ftest_generator(filePath):
    def test(self=None):
        """ Test failes if Exception in execution of f. """
        if self is not None:
            print(filePath)
            imp.load_source(os.path.basename(filePath)[:-3], filePath)
    return test

for k, f in enumerate(py_files):
    test_name = 'test_{:03d}_{}'.format(k, os.path.basename(f)[:-3])
    test_name = test_name.replace('.', '_')
    test = ftest_generator(f)
    setattr(PythonExampleTestCase, test_name, test)


if __name__ == '__main__':
    unittest.main()

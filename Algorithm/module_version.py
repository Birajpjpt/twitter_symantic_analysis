import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn

class version:
    def printVersion(self):

        print('Python: {}'.format(sys.version))
        # scipy
        print('scipy: {}'.format(scipy.__version__))
        # numpy
        print('numpy: {}'.format(numpy.__version__))
        # matplotlib
        print('matplotlib: {}'.format(matplotlib.__version__))
        # pandas
        print('pandas: {}'.format(pandas.__version__))
        # scikit-learn
        print('sklearn: {}'.format(sklearn.__version__))

x = version()
x.printVersion()
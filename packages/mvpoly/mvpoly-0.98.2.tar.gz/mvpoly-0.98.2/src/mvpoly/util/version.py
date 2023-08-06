# some tools for versions of libraries

import scipy.version
import numpy.version
from pkg_resources import parse_version


def at_least(libstr, req):
    if libstr == 'scipy':
        ver = scipy.version.version
    elif libstr == 'numpy':
        ver = numpy.version.version
    else:
        raise ValueError("library {0!s} not known".format((libstr)))
    return parse_version(req) <= parse_version(ver)

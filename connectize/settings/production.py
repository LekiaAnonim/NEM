from .base import *

import environ

DEBUG = False

try:
    from .local import *
except ImportError:
    pass



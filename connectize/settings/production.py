from .base import *

import environ

DEBUG = False

ALLOWED_HOSTS = ["nem-production.up.railway.app", "connectize.co"]

try:
    from .local import *
except ImportError:
    pass



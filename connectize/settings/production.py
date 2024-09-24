from .base import *

import environ



env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')
ALLOWED_HOSTS = ["nem-production.up.railway.app", "connectize.co", 'localhost:3000', 'connectize-drab.vercel.app']

EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 2525
EMAIL_HOST_USER = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

try:
    from .local import *
except ImportError:
    pass



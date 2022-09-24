from decouple import config
from .base import *

# SECURITY WARNING: could be any secret key
SECRET_KEY = config('SECRET_KEY2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [*]

STATIC_URL=
STATIC_ROOT=
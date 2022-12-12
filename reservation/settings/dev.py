from decouple import config
from .base import *

# SECURITY WARNING: could be any secret key
SECRET_KEY = config('SECRET_KEY2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#STATIC_URL=
#STATIC_ROOT=


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =config('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')



# Emailing settings


PASSWORD_RESET_TIMEOUT = 14400



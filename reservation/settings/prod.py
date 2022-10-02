#from decouple import config
from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['120.0.0.1:2000','127.0.0.1']

#AW settings

#AWS_ACCESS_KEY_ID=config("AWS_SECRET_ACCESS_KEY")
#AWS_STORAGE_BUCEKT_NAME=config("AWS_STORAGE_BUCEKT_NAME")
#AWS_S3_....


#Heroku settings

#Heroku logging
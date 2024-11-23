import os
from .common import *

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# # # --- Move to dev.py, prod.py
# PRODUCTION DB
DATABASES = {
    
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_basic_db',
        'USER': 'admin',
        'PASSWORD': 'admin1234',
        'HOST': 'localhost',  # or your PostgreSQL host
        'PORT': '5432',        # default PostgreSQL port
        # 'ATOMIC_REQUESTS': True  # Applay transaction for every request
    }
}

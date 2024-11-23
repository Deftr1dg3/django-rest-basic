from .common import * 


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-92%dq9-^+%*&&f00&zvrr%rpzppxh6zdmrc+=pv)s-x_ul08*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Only required if DEBUG is True
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# # # --- Move to dev.py, prod.py
# DEVELOPMENT DB
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

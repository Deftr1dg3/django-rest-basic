# DJANGO ------------------------------------------

## 1. Install Django and Django REST framework:

% pip install django djangorestframework

## 2. Start Django project:

% django-admin startproject [project name] .

## 3. Create Django app:

% django-admin startapp [app name]

## Then needs to add created apps and rest_framework

## to the project settings:

% [project name] -> settings.py -> INSTALLED_APPS

add app:

'[app name].apps.[the only class name]'

rest framework:

'rest_framework'

# Create urls.py in Created app and connect to the project

Import to project and app urls.py files

- from django.urls import path, include

In project urls.py

urlpatterns = [
path('admin/', admin.site.urls),
path('demo/', include('demo.urls'))
]

In app urls.py

urlpatterns = [
path('home', views.home, name='home')
]

## 4. Once made changes to the model or to the database

next command has to be run:

% python ./manage.py makemigrations
this will create sqlite3 database to store
all settings

% python ./manage.py migrate
this will apply settings and cretae default database SQLite of not
specified custom DB.

    Make common dir with templates on project level.
    Updatte TEMPLATES['DIRS'] in settings.py
    Provide absolute path to the 'templates' directory.

    TEMPLATES {
        ...
        'DIRS' : [str(BASE_DIR.joinpath('templates'))]
        ...
    }

## 5. Run server

% python ./manage.py runserver [host]:[port]
Development only
On production use Gunicorn or Gunicorn + Unicorn for ASGI

% gunicorn -w 4 -b 0.0.0.0:8000 myproject.wsgi:application

## 6. Create Django usr (in order to use Admin Panel)

% python ./manage.py createsuperuser
Then follow instruction on the screen

## 7. Tests

    Cretae test cases in test.py file in the app dir.
    Inherit test class from 'SimpleTestCase' for test
    that do not involve database requests.
    Inherit from 'TestCase' if DB is used.

    Common use 'TestCase' for both options.

    Run test:
    % python manage.py test

## Prepare static files for poduction:

Add to settings.py:

STATIC_URL = "static/"

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]

STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

- Run command:
  $ python manage.py collectstatic

- While there are multiple ways to serve these compiled static files in production, the most
  common approach–and the one we will use here–is to introduce the WhiteNoise116 package.

$ pipenv install whitenoise==5.1.0

Then in config/settings.py there are three updates to make:
• add whitenoise to the INSTALLED_APPS above the built-in staticfiles app
• under MIDDLEWARE add a new line for WhiteNoiseMiddleware
• change STATICFILES_STORAGE to use WhiteNoise

STATICFILES_STORAGE =
'whitenoise.storage.CompressedManifestStaticFilesStorage'

$ python manage.py collectstatic

## 100. Get access to django shell

% python manage.py shell
Allows to add items to the database

    % from app.models import [the model]
    % inst = Model(**kwargs)

    Save to database

    % inst.save()

    List all objects of the model

    % Model.objects.all()

    Get line by column name

    % inst = [Model Name].objects.get(id=..., || name=...)

    Get Set of Items that stored in different model
    by FK related to current model

    % inst.item_set.all()

    Add new item into the set

    % inst.item_set.create(arg1="", arg2="", ...)

# See Rqw SQL query ----

```python
# Execute custom SQL
raw_query = "SELECT * FROM store_customer WHERE first_name = %s"
queryset = Customer.objects.raw(raw_query, ['Dory'])

# See raw SQL
print(f'\nRAW SQL QUERY:\n{queryset.query}\n')

# Modifying SQL Queries with Extra Clauses -- DEPRICATED
# If you need to add extra SQL clauses or annotations, you can use .extra()
# with Django’s ORM to append custom SQL conditions without going fully raw.

queryset = MyModel.objects.extra(
    select={'custom_field': 'SELECT COUNT(*) FROM another_table WHERE another_table.id = myapp_mymodel.id'},
    where=['myapp_mymodel.field_name = %s'],
    params=['example']
)
print(queryset.query)  # To see the modified SQL
```

To see and modify raw SQL queries in Django:

Use .query on a queryset to see generated SQL.
Use .raw() for custom SQL execution.
Use .extra() for additional SQL clauses.
Use Django Debug Toolbar or logging for debugging.

32. Create superuser in django

python manage.py createsuperuser

33. Disable all username and password validations:

Add next row to settings.py file

```python
AUTH_PASSWORD_VALIDATORS = []
```

34. Change admin password in terminal

python manage.py changepassword admin

35. Register models

Go to the desired app folder > admin.py

REGISTER:

```python
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Collection)
admin.site.register(models.Product)
...
...
...
```

Best practice with ability to make custome changes:

```python
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    # Override parent class method
    # to get needed results
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            products_count = Count('product')
        )
        return queryset
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
```

# Django Debug Toolbar ----------------------------

## 1.Install Django Debug Toolbar

    % pip install django-debug-toolbar

## 2. Add debugger to the applications list in the

## settings.py

add - 'debug_toolbar'

## 3. Add debugger to the main urls.py

```python
import debug_tools

...
...
urlpatterns = [
    # ...
    path("__debug__/", include("debug_toolbar.urls")),
]
```

## 4. Add debugger to the MIDDLEWARE in settings.py

```python
MIDDLEWARE = [
...
"debug_toolbar.middleware.DebugToolbarMiddleware",
...
]
```

## 5. Insert into settings.py

```python
INTERNAL_IPS = [
...
"127.0.0.1",
...
]
```

## 6. Applay all changes befor you start using the

## debugger. Otherwise an Error will appear.

    $ python manage.py makemigrations
    $ python manage.py migrate

# Second Debug option - .vscode/launch.json file

Create file if not exists and add next content to the file:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver", "--noreload"],
      "django": true,
      "justMyCode": true,
      "console": "integratedTerminal",
      "env": {
        "DJANGO_DEBUG": "1"
      }
    }
  ]
}
```

OR

Go to > Debug Panel on the Let side > choose "create launch.json" file > choose Pytho ... from dropdown at the top

> choose Django Launch and Debug.

# Django TESTS With QODO----------------------------

Ensure that DJANGO_SETTINGS_MODULE environment variable is set,
before running tests.

export DJANGO_SETTINGS_MODULE=[project_name].settings

## For pytest add "pytest.ini" file to the root dir where is "manage.py" located

With next content:

    [pytest]
    DJANGO_SETTINGS_MODULE=config.settings
    python_files = test.py test_*.py *_test.py

## Or "conftest.py"

With next content:

    import os
    import pytest

    from django.conf import settings

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

    import django
    django.setup()

    @pytest.fixture(autouse=True)
    def enable_db_access_for_all_tests(db):
        pass

@pytest.mark.django_db (on function or class): This marker tells pytest that the test
will interact with the database.
It sets up and tears down the test database for each test.

Run pytest:

    $ pytest

    or

    $ pytest -v

    or Run cpecific file:

    $ pytest your_app/tests/test_cart.py

    or Run specific function:

    $ pytest your_app/tests/test_cart.py::test_add_cart_item_with_zero_quantity

    or Show Detailed Traceback:

    $ pytest --tb=long

Advance:

    For measuring test coverage:
    pytest-cov
    pip install pytest-cov
    pytest --cov=your_app tests/

    For parallel test execution:
    pytest-xdist
    pip install pytest-xdist

    Run tests in parallel:
    pytest -n auto

    pytest-django

    pytest-benchmark

    pytest-behave

# Database Migrations to Django Project ---------------------------

To SQL code of migration use:

    python manage.py makemigrations

    python manage.py migrate

See SQL request of migration:

    python manage.py sqlmigrate [name_of_app] [number_of_migration]

Show migrations:

    python manage.py showmigrations

To revert only the last migration of a specific app, you can run the following command:

    python manage.py migrate <app_name> <previous_migration>

This command tells Django to revert all
migrations for that app back to "zero," effectively
rolling back all migrations for that app.

    python manage.py migrate your_app_name zero

# Connect PostgreSQL to Django project ---------------------------------------------------

Run the following command to install the PostgreSQL adapter for Python:

    pip install psycopg2

    psycopg2 is a PostgreSQL adapter for Python, and it is necessary when using
    Django with a PostgreSQL database because it allows Django
    to communicate with PostgreSQL

Update settings.py: In your Django project’s settings.py file,
configure the DATABASES setting as follows:

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',  # or your PostgreSQL host
        'PORT': '5432',        # default PostgreSQL port
    }

}

# Custom SQL ------------------------------------------------

1. Create an empty migration:

   python manage.py makemigrations <table_name> --empty

Use migrations.RunSQL(sql="""""", reverse_sql="""""") in the
empty migration under "operations" fiels.
sql -> Raw SQL that will be executed in "mograte" command.
reverse_sql -> Raw SQL that will be executed on roll back.

Example new empty migration file content:

    from django.db import migrations

```python
class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_customer_idx_last_name_first_name'),
    ]

    operations = [
        migrations.RunSQL(sql="""
        INSERT INTO store_collection (title) VALUES('collection1')
        """,
        reverse_sql="""
        DELETE FROM store_collection WHERE title='collection1'
        """)
    ]
```

### REDIS FOR CELERY ----------------------------

Run in docker container
and install via pip: pip insatll redis

name: redis, port 6379

### CELERY ---------------------------

pip install celery

run in terminal to start worker process:

    celery -A <packasge_name or modeule_name> worker --loglevel=info(for development)

-A - application.

If you use packge name, import
Celery app from its module to **init**.py in the target package

To start beat (scheduled tasks execution) process:

    celery -A config beat

# Flower to monitor celery processes ---------------

    pip install flower

To start flower process:

    celery -A <name> flower

You can access it on localhost:5555

### TESTS --------------------

pip install pytest pytest-django
pip install model-bakery

model_bakery is a package used for creating test data in Django applications.

Naming conventions.

PyTest will look for a folder 'tests' (in plural form, it is important)

Names of files in tests folder should start with 'test\_'

Names of test function should start with 'def test\_'

Name of the function has clearly describe the behaviour you are testing.
Example:

def test_if_user_anonimus_returns_401():
...

Because during the testing you can see names of the functions only.
And you should understand by the name where the issue occures.

Use classes to gather tests with main purpose.
Example:

```python
class TestCreateCollection:
    def test_if_user_anonimus_returns_401():
        ...

    def test_if_user_not_admin_returns_403():
        ...

```

Every test has to have three parts -> 'AAA' triple A

Arrange, Act, Assert

Arrange:
Initial part. Creating objects, preparing data, etc

Act:
Behavious we want to test
client = APIClient()

# Always add forward slash to the end of the path, otherwise

# you'll get an error

client.post('/store/collections/')

Assert:
Checking if the behaviour to be exepect is
what actually happens.

To setup pytest, create 'pytest.ini' file in the root directory of the project
Example:
[pytest]
DJANGO*SETTINGS_MODULE=config.settings
filterwarnings =
ignore::django.utils.deprecation.RemovedInDjango60Warning
; python_files = test.py test*_.py _\_test.py
; benchmark-autosave = true
; benchmark-min-rounds = 5
; benchmark-max-time = 1.0 # Stop after 1 second

Errors:
The errors you're seeing indicate that there is a missing module called model_bakery that is required by your test files.
model_bakery is a package used for creating test data in Django applications.

pip install model-bakery

Execute tests:

$ pytest -> to execute all tests in project

$ pytest store/tests -> executes tests only in specified dir

$ pytest store/tests/test_collection.py -> test specified module only

$ pytest store/tests/test_collection.py::TestCreateCollection -> test specified class only

$ pytest store/tests/test*collection.py::TestCreateCollection::test*... -> test specified method only

$ pytest -k anonimus -> executes all tests that have 'anonimus' in their names

Skipping some tests:

apply decorator @pytest.mark.skip on desired test

### Continuous testing ----------------

pip install pytest-watch

Execute $ ptw instead of $ pytest in separate Terminal window.
This will run all tests and rerun them every time you change the code.

# Configure tests in VSCode:

Click in lask image on the left panel -> Configure Python Tests -> pytest -> Root directory
Thi wil pickup all tests form all apps.

# Use pytest.fixtures to remove duplicates in code.

For global Fixtures in the app:

Create 'conftest.py' in 'tests' dir file.
Fixtures or othe structures defined in this file, pytest will load automatically.

Example:

```python
from rest_framework.test import APIClient

import pytest


@pytest.fixture
def api_client():
    return APIClient()

```

In this example fixture api_client() will be created once and will
be available in all tests.

The fixture will be passed to the test function as an argument:

```python
def test_if_data_is_invalid_returns_400(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))
        response = cast(Response, api_client.post('/store/collections/', {'title': ''}))
```

For local fixtures in the module:

Create function in the same module on the top
Example of fixture with ability to pass arguments

```python
@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        response = api_client.post('/store/collections/', collection)
        return response
    return do_create_collection
```

## Use model_bakery to create models withous fullfilling all the fields

ALWAYS USER '/' IN THE END OF THE ADDRESS.
OTHERWISE YOU WILL GET 301 ERROR.

Becase django automatically redirects all '/path/to/resource' to '/path/to/resource/'

```python
@pytest.mark.django_db
class TestRetriveCollaction:
    def test_if_collection_exists_returns_200(self, api_client):
        # Arrange
        # First create collection
        # collection = Collection.objects.create(title='Test')
        # we can use model_bakery to avoid fullfilling all fields in the model
        collection = baker.make(Collection)

        # # example, creating 10 products in the same collection
        # products = baker.make(Product, collection=collection, _quantity=10)
        # Act
        response = api_client.get(f'/store/collections/{collection.id}/') # type: ignore
        # Assert
        assert response.status_code == status.HTTP_200_OK
        # assert response.data['id'] == collection.id # type: ignore
        # assert response.data['title'] == collection.title # type: ignore
        # better way to compare
        assert response.data == {
            'id': collection.id,
            'title': collection.title
        }
```

### Performance testing -------------------------

Locust - performance testing tool with UI

pip install locust

Create 'locust' folder with testing modules like 'brows_products.py', 'user_auth.py', etc

Run Locust:

locust -f <folder>/<file_name>

locust -f locust/brows_products.py

### OPTIMIZATIONS ---------------------------------

# OPTIMIZATIONS -----------------------------------

# In most of the cases to optimize performance needs to optimize

# either request or the DB itself.

# Request optimizations --------

# Preload related objects

# One to many, OneToOne

Product.objects.select_related('...')

# Many To Many, Reverse Relation

Product.objects.prefetch_related('...')

# Load only what you need

Product.objects.only('title')

# Oposit of .only()

Product.objects.defer('description')

# Use values

# Get dictionary

Product.objects.values()

# Get list

Product.objects.values_list()

# Creating dict or list cheaper from creating Django Model

# So if you do not need specific bahavious of Django Model

# like create, update, delete, etc. Use those methods.

# Count Properly

Product.objects.count() # Proper way to count objects
len(Product.objects.all()) # BAD practice

# Bulk create/update

Product.objects.bulk_create([])

### Django_silk -------------------

Profiling tool used to identify bottle necks in the app

URL: https://github.com/jazzband/django-silk

> $ pip install django-silk

Add silk to INSTALLED_APPS:

INSTALLED_APPS = [
...
'silk',
]

Add silk to MIDDLEWARE:

MIDDLEWARE = [
'silk.middleware.SilkyMiddleware',
...
]

Add silk to URL patterns:

urlpatterns = [
...
path('silk/', include('silk.urls', namespace='silk')),
]

RUN MIGRATIONS:

> $ python manage.py migrate

visit 'domain/silk' path

POSSIBLE CONFIGURATIONS in 'settings.py' file:

```python
SILKY_PYTHON_PROFILER = True  # Enable Python profiling
SILKY_META = True            # Capture metadata about requests
SILKY_MAX_RECORDED_REQUESTS = 1000  # Limit the number of requests stored
SILKY_INTERCEPT_PERCENT = 100  # Percentage of requests to intercept (default: 100%)
```

### CACHING --------------------------------------

Redis
Run in docker container
and install via pip: pip insatll redis

name: redis, port 6379

To use Redis thogether with Django we should also install library called django-redis

$ pip install django-redis

URL: https://github.com/jazzband/django-redis

Cache configuration for settings.py from the URL GitHub:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

## Execute commands directly in Redis container

docker exec -it redis_container redis-cli

> select <db_numbe>r - to select databases in range 0 - 15

> 127.0.0.1:6379> select 2

> keys \* - view all keys in DB

> 127.0.0.1:6379[2]> keys \*

> del <key_name> - delete key

> flushall - delete all the data

### Prepearing for production ----------------------------------------------------

While DEBUG is True Django collects static file automatically.
But for Production to collect statuic files needs to add a settings into
the settings.py file

STATIC_URL = '/static/'

# Settings up STATIS ROOT to let the Django know

# where the static files located on disk

# Thes will allow to collect static files from different apps to one place

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Then runcommand in terminal to collect the file to the 'static' folder in main dir:

## RUN THIS COMMAND EVERY TIME BEFORE DEPLOY ---------

> $ python manage.py collectstatic

## INstall 'whitenoise' library to serve 'static' files in production

> $ pip install whitenoise

Add 'whitenoise' to the middleware, as high as possible, but after 'Security Middleware':

MIDDLEWARE = [
'...',
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware',
...
]

### Configure logging ----------

Add to 'settings.py' file

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{', # This allows the use of `{}`-style formatting
        },
        'detailed': {
            'format': '{levelname} {asctime} {pathname} {funcName} {lineno} {message}',
            'style': '{',   # str.format()
            # 'style': '$'  # string.Template class
        }
        },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/Users/stasusbondevito/Documents/PYTHON/Learning/Django/logging_in_django/src/logs.log',
            'formatter': 'simple',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'demo': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # # With empty string instead of the name
        # # The logger willcapture all logs from all the apps
        # # Used in most of the cases.
        # '': {
        #     'handlers': ['file', 'console'],
        #     'level': os.environ.get('DJANGO_DEBUG_LEVEL', 'INFO'),
        #     'propagate': True,
        # }
    }
}

```

### Production Settings ------------------------------------------------------------

Store all sensetive information in environment variables !!!

Setting UP:

Create 'settings' folder in 'config' dir
Move 'settings.py' to the 'settings' folder
Remane file to 'common.py'

Cretae specified files for different purposes:

dev.py, prod.py, ...

At the first line of each file import all from common.py:

> $ from .common import \*

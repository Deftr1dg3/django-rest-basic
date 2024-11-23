import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

celery = Celery('storefront')
# Specify where celery can find configuration variables
celery.config_from_object('django.conf:settings', namespace='CELERY')
# Set the broker_connection_retry_on_startup setting properly
celery.conf.broker_connection_retry_on_startup = True
# Will automatically discover tasks.py modules
celery.autodiscover_tasks()




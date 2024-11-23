from django_filters.rest_framework import FilterSet
from .models import Product


# Generic filtering using third party django-filter library.
# Add 'django_filters' to INSTALLED_APPS. The name of the app is different
# from the name of the module - 'django-filter'
# Use 'pip install django-filter' to install the module
class ProductFilter(FilterSet):
    class Meta:
        model = Product 
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],
            'inventory': ['gt', 'lt'] 
        }
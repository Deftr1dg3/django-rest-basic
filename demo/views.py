from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Count
from django.db import transaction
from django.db.models.aggregates import Max, Min, Sum, Avg
from django.db.models import Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db import connection
# For generic content type 
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem, Tag

from store.models import Product, Customer, Collection, Order, OrderItem

# email 

from django.core.mail import send_mail, send_mass_mail, mail_admins, BadHeaderError, EmailMessage
# To send templated emails 
from templated_mail.mail import BaseEmailMessage
# To execute background tasks 
from .tasks import notify_customers
# To for caching examples
import requests 
from django.core.cache import cache 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response 
# For logging 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

# SETTING UP LOGGING ------------------------------

logger = logging.getLogger(__name__) # __name__ = demo.view (Name of the module)


class LoggingView(APIView):
    def get(self, request):
        try:
            logger.info('Getting info from http://httpbin.org')
            response = requests.get('http://httpbin.org/ip')
            data = response.json()
            logger.info('Got info from http://httpbin.org/ip')
        except Exception as ex:
            logger.error(msg=str(ex))
            # return Response()
            return Response({'error': str(ex)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(data)

    def post(self, request):
        logger.error('POST method used')
        return Response({"message": "Hello, this is a POST request!"})

    def put(self, request):
        logger.info('PUT request')
        return Response({"message": "Hello, this is a PUT request!"})

    def patch(self, request):
        logger.info('PATCH request')
        return Response({"message": "Hello, this is a PATCH request!"})

    def delete(self, request):
        logger.info('DELETE request')
        return Response({"message": "Hello, this is a DELETE request!"})

    def options(self, request):
        logger.info('OPTIONS request')
        return Response({"message": "Hello, this is an OPTIONS request!"})

    def head(self, request):
        logger.info('HEAD request')
        return Response({"message": "Hello, this is a HEAD request!"})
    
    def trace(self, request):
        logger.info('TRACE request')
        return Response({"message": "Hello, this is a TRACE request!"})
    
    def connect(self, request):
        logger.info('CONNECT request')
        return Response({"message": "Hello, this is a CONNECT request!"})
    


# Create your views here.

# CACHING --------------------------------------------------------------

class Demo(APIView):
    
    @method_decorator(cache_page(10 * 60))
    def get(self, request):
        response = requests.get('http://httpbin.org/delay/2')
        data = response.json()
        return Response(data)
 

# Storing the result of the view itself
# Applicable for function based views only
# @cache_page(20)
# def caching_example(request):
#     response = requests.get('http://httpbin.org/delay/2')
#     data = response.json()
#     return JsonResponse(data)



# # So called Low Level caching :)))
# def caching_example(request):
#     cache_key = 'httpbin_result'
#     if cache.get(cache_key) is None: 
#         response = requests.get('http://httpbin.org/delay/2')
#         data = response.json()
#         # Third argument is timeout in seconds 10 * 60 = 10 min.
#         cache.set(cache_key, data, 20)
#     else:
#         data = cache.get(cache_key)
#     return JsonResponse(data)



# SENDING EMAILS -------------------------------------------------------
# BadHeaderError raises once spoofing attack performed

def background_task(request):
    notify_customers.delay('Hello World')
    return HttpResponse('Task execution started')


def send_email(request):
    try:
        # For bulk users use send_mass_mail
        # send_mail('subject', 'message', 'info@seth.com', ['boob@mike.com', 'alice@hike.com'])
        
        # For Admins 
        # mail_admins('subject', 'message', html_message='message_html')
        
        # Customer amil message object. Attaching file
        # message = EmailMessage('subject', 'message', 'fraud@money.com', ['me@seth.com'])
        # message.attach_file('demo/static/images/cat_with_guitar.jpg')
        # message.send()
        
        # Insatll django-templated-mail to be able to create templates ------
        # The template has to be in 'templates' folder
        message = BaseEmailMessage(
            template_name='hello.html',
            context={
                'name': 'Seth Bergon'
            }
        )
        # message.attach_file('demo/static/images/cat_with_guitar.jpg')
        message.send(['me@mike.com', 'and_me_again@mosh.com'])
    except BadHeaderError:
        pass
    return HttpResponse('Email Sent')



# BASIC model operations ----------------------------------------------------------------

# @transaction.atomic
def home(request):
    queryset = None
    result = None
    
    # Use Q() object (encapsulates condition) if you need to use OR operator 
    # '~' used as NOT operator: ~Q(unit_price__lt=20) == Q(unit_price__gte=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)).values()
    
    # F() object references particular field. That allows
    # to compare fields from the same table 
    # query_set = Product.objects.filter(inventory=F('unit_price')).values()
    
    # query_set = Product.objects.filter(collection__id=4).order_by('unit_price').reverse().values()
    
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id')).order_by('title')
    
    # select_related - JOIN (One To Many) - returns the value Django stores in reverse fielt pointing
    # to the table the has One To Many collaction to current table.
    
    # prefetch_collection - JOIN (Many To Many) - return collection
    # query_set = Product.objects.select_related('collection').all()
    
    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    
    # Agreagate functions
    
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'), max_price=Max('unit_price'), total_price=Sum('unit_price'))
    
    # result = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))
    
    # result = OrderItem.objects.filter(product__id=1).aggregate(total_prod_1_sold=Count('product__id'))
    
    # result = OrderItem.objects.filter(order__customer__id=1).aggregate(customer_1_made=Count('order__customer'))
    
    # products = list(query_set)
    
    # Add additional column with Value = True
    # result = Customer.objects.annotate(new_id=Value('22')).values()
    # result = Customer.objects.annotate(new_id=F('id') + 1).values()
    
    # Functions
    # result = Customer.objects.annotate(
    #     full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )
    # result = Customer.objects.annotate(
    #     full_name = Concat('first_name', Value(' '), 'last_name')
    # )
    
    # queryset = Customer.objects.annotate(
    #     orders_placed=Count('order')
    # ).order_by('id')
    
    # Expression wrapper
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )
    
    # queryset = Customer.objects.annotate(
    #     total_spent=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity'))
    # ).order_by('id')
    
    # queryset = Product.objects.filter(orderitem__isnull=False).annotate(
    #     total_sale=Sum(F('orderitem__unit_price') * F('orderitem__quantity'))
    # ).order_by('-total_sale')[:5]
    
    # For Generic contant types 
    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggetItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #     content_type=content_type,
    #     object_id=1
    # )
    
    # Generic content type using custom manager, located in tags.models.py
    
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)  # type: ignore
    
    # Execute customer SQL 
    # raw_query = "SELECT * FROM store_customer WHERE first_name = %s"
    # queryset = Customer.objects.raw(raw_query, ['Dory'])
    # .extra() - depricated
    # or
    # use 'with' statement or try .. finally blocks
    # cursor = connection.cursor()
    # cursor.execute('RAW SQL HERE')
    # cursot.close()
    # with connection.cursor() as cursor:
    #   cursor.execute('RAW SQL HERE')
    #   or we can call Stored Precedure better way
    #   cursor.callproc('proc_name', ['parameters', 'here'])
    
    # # See raw SQL 
    # print(f'\nRAW SQL QUERY:\n{queryset.query}\n')
    
    # print(f'RESPONSE TYPE = {type(queryset)}')
    
    queryset = Collection.objects.all()
    
    return render(request, 'home.html', {'iterable': queryset, 'result': result})



def create(request):
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=3)
    # collection.featured_product_id = 3
    # collection.save()
    # or
    # collection = Collection.objects.create(title='Video Games', featured_product_id=1)
    
    # collection = Collection.objects.all()
    
    cart = Order()
    cart.id = 1001 # type: ignore
    cart.customer_id = 1 # type: ignore
    cart.save()
    
    item1 = OrderItem()
    item1.id = 1001 # type: ignore
    item1.order = cart 
    item1.product_id = 1 # type: ignore
    item1.quantity = 1
    item1.unit_price = 199.99 # type: ignore
    item1.save()
    
    
    return render(request, 'home.html', {'iterable': [item1], 'result': 201})


def update(request):
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()
    # or
    # Collection.objects.filter(pk=11).update(featured_product = Product(pk=23))
    
    item = OrderItem.objects.get(pk=1001)
    item.quantity = 42
    item.save()
    
    return render(request, 'home.html', {'iterable': [200], 'result': None})
    
def delete(request):
    # collection = Collection(pk=10)
    # collection.delete()
    # Collection.objects.filter(pk=10).delete()
    # Collection.objects.filter(id__gt=5).delete()
    
    # cart = Order(pk=1)
    # cart.delete()
    
    Order.objects.filter(id__gt=1004).delete()

    return render(request, 'home.html', {'iterable': None, 'result': 200})


# Use to wrap in the transaction all the ocde inside the function.
# @transaction.atomic()
def transaction_example(request):
    # ID = 1005
    with transaction.atomic():
        order = Order()
        # order.id = ID
        order.customer_id = 1 # type: ignore
        order.save()
        
        item = OrderItem()
        # item.id = ID
        item.order = order 
        item.product_id = 13 # type: ignore
        # raise Exception('ex')
        item.quantity = 45
        item.unit_price = 16.99 # type: ignore
        item.save() 
    
    return render(request, 'home.html', {'iterable': None, 'result': 200})


def add(a, b):
    allowed_data_types = {int, float}
    if not type(a) in allowed_data_types or type(b) not in allowed_data_types:
        raise TypeError('The function accepts argumens of types int and float only.')
    return a + b
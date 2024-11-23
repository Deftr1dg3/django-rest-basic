from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import AbstractUser, BaseUserManager

# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import DestroyAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser,DjangoModelPermissions

from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer 
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer
from .serializers import UpdateCartItemSerializer, CustomerSerializer
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .serializers import ProductImageSerializer

from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Order, Customer
from .models import ProductImage

from .filters import ProductFilter
from .pagination import ProductPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission

# Create your views here.


# Use ViewSets instead of two next classes ---------
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    # Generic filtering ---------
    # Generic filtering using third party django-filter library
    # Add 'django_filters' to installed app. The name of the app is different
    # from the name of the module - 'django-filter'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id', 'inventory', 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    # Pagination: PageNumberPagination - page number, 
    # LimitOffsetPagination - Limit Offset pagination
    pagination_class = ProductPagination
    
    permission_classes = [IsAdminOrReadOnly]
    
      
    # Filtering logic for predefined fields ---------
    # def get_queryset(self) -> QuerySet:
    #     self.request: Request
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id', None) 
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__id=kwargs['pk']).count() > 0:
            return Response({"error": "Product can not be deleted because is is associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# class ProductList(ListCreateAPIView):
    
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    
    # Override methods in Generic View if you want to add some logic 
    # otherwise use class fields like: 
    # def get_queryset(self):queryset, serializer_class, ...
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}
    
        
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     # queryset = Product.objects.all()
#     # serializer_class = ProductSerializer
#      # Override lookup_field if you use variable different from pk
#     # lookup_field = 'pk'
    
#     # Override methods like 'get', 'post', 'delete', etc if you need custom functionality
#     def delete(self, request, pk):
#         product: Product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0: # type: ignore
#             return Response({"error": "Product can not be deleted because is is associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
  
  
# Use ViewSets instead of two next classes ---------
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection__id=kwargs['pk']).count() > 0:
            return Response({"error": "The collection can not be deleted because it contains one or more product"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
# class CollectionList(ListCreateAPIView):    
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer
#     # Override lookup_field if you use variable different from pk
#     # lookup_field = 'pk'
    
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0: # type: ignore
#             return Response({"error": "The collection can not be deleted because it contains one or more product"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self) -> QuerySet:
        queryset = Review.objects.filter(product_id=self.kwargs['product_pk']).all()
        return queryset
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    


#  Cart ---------------------------------------------

class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer 
    

class CartItemViewSet(ModelViewSet):
    http_method_names  = [
        'get',
        'post',
        'patch',
        'delete'
    ]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')
    
    
    
# class CartList(CreateAPIView, DestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
    
    
    
# class CartList(APIView):
    
#     def get(self, request):
#         return Response('ok')
    
#     def post(self, request):
#         serializer = CartSerializer(data={})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)




#  Authentication -------------------------------------------------
#  DJOSER django authentication library for wprk with JWT tokens
# To see all endpoints provided by DJOSER visit https://djoser.readthedocs.io/
# $ pip install -U djoser
# $ pip install -U djangorestframework_simplejwt - To work with JWT
# $ pip install -U social-auth-app-django - To use third party based authentication
# 
# Installation process may be changed, check the latest docks every time.

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    # Higher level of control 
    # permission_classes = [FullDjangoModelPermissions] 
    
    # @action()
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
    
    # Return permission objects
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
        
    
    # def get_permission(self, request):
    #     if request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    
    # Action with custom permission
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')
        
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # If user is not authorized it will be set to an instance of AnonymusUser class
        # AUTH middleware checks if request contains user data like id,
        # retrives the user from the db and attaches it to the request as request.user
        # request.user
        
        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        customer = Customer.objects.get(user_id=request.user.id)
  
        if self.request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif self.request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# ORDER --------------------------------------------------------------------------------


class OrderViewSet(ModelViewSet):
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options'
    ]
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        self.request: Request
        user = self.request.user
        if user.is_staff: 
            return Order.objects.all()
      
        # queryset =  Order.objects.filter(customer_id=user.customer_id) # type: ignore
        # or another way to retrive customer_id from User 

        customer_id = Customer.objects.only('id').get(user_id=user.id) # type: ignore
        if not customer_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset = Order.objects.filter(customer_id=customer_id)
   
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    
#  Product Images API --------------------------------------------------

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer 
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    

# # OPTIMIZATIONS -----------------------------------

# # In most of the cases to optimize performance needs to optimize
# # either request or the DB itself.

# # Request optimizations --------

# # Preload related objects 
# # One to many, OneToOne
# Product.objects.select_related('...')
# # Many To Many, Reverse Relation
# Product.objects.prefetch_related('...')

# # Load only what you need
# Product.objects.only('title')
# # Oposit of .only()
# Product.objects.defer('description')   

# # Use values 
# # Get dictionary
# Product.objects.values()
# # Get list
# Product.objects.values_list()
# # Creating dict or list cheaper from creating Django Model
# # So if you do not need specific bahavious of Django Model
# # like create, update, delete, etc. Use those methods.

# # Count Properly 
# Product.objects.count() # Proper way to count objects
# len(Product.objects.all()) # BAD practice

# # Bulk create/update
# Product.objects.bulk_create([])

    
    
# TOKENS -------------------------

# JOHN
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjI3NTc4MCwiaWF0IjoxNzMxODQzNzgwLCJqdGkiOiJlYTFhOWU5ZjgyM2U0MjEyODViNjY5ZDcyY2U5MWRlNiIsInVzZXJfaWQiOjJ9.XVYX5sqt9C23NpM5Nj9tNvUne2CcBcb9KxO4gIwFzks",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMTkzMDE3LCJpYXQiOjE3MzE4NDM3ODAsImp0aSI6ImU3MzE0MTI4NmU2NTRlM2U4M2RlN2ZjMGNkN2I5MmFiIiwidXNlcl9pZCI6Mn0.SZIROCVqji57cdp8WCxg699WLX0CfHPJJPf_kysJzd0"
# }

# USER2
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjI3NTg5OCwiaWF0IjoxNzMxODQzODk4LCJqdGkiOiJlZTlmYmRlMmYzMDk0MzEyYjNmYmNmYjM5ZmRiYjY1MyIsInVzZXJfaWQiOjR9.xCH3sIV9M3EZ6x4BlqoT6HIZdnDd9S8sf2HRVxhnsbE",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMTkzMjIyLCJpYXQiOjE3MzE4NDM4OTgsImp0aSI6ImZlZGM1OTJhNTEyNTRhODI5OGE0YjliYmVjOGUwYzUyIiwidXNlcl9pZCI6NH0.5yEU55hOkWzolGhW_4CxB7FZaLj6JU-p1haj99r_Ic4"
# }

# USER4

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjI3NTk0MSwiaWF0IjoxNzMxODQzOTQxLCJqdGkiOiIwYTZiOWI1ODU4ZWY0ZGZmYmQyNmM0NTQwYzg1ODk3ZCIsInVzZXJfaWQiOjZ9.IYuuQmsddcjbFsu8CGLo1_oWArmNNi_l5ooO-OLp63w",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxOTMwMzQxLCJpYXQiOjE3MzE4NDM5NDEsImp0aSI6IjY3MjM0ZWFmMDNkODRjMDg4NDlhNWNjYzE5NGFlZDg0IiwidXNlcl9pZCI6Nn0.CQoKAginhoCJQzEjPaZZQl7jzkCPw2rTjI1kfXdKlMk"
# }


# admin 

#  FUNCTION BASED VIEWS -------------------------------------------------------------------------------------


# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # data = serializer.validated_data
#         # print(f'DATA: {data}')
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_details(request, id):
#     product: Product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0: # type: ignore
#             return Response({"error": "Product can not be deleted because is is associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
   

# @api_view(['GET', 'POST'])     
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(
#             products_count=Count('products')
#         ).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_details(request, id):
#     collection: Collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count('products')).all(), 
#         pk=id)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0: # type: ignore
#             return Response({"error": "The collection can not be deleted because it contains one or more product"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)












# Post examples 

# {
#     "title": "prod",
#     "slug": "prod-1",
#     "unit_price": 99.99,
#     "inventory": 57,
#     "collection": 6
# }

# {
#     "id": 1010,
#     "title": "prod_2",
#     "slug": "prod-2",
#     "description": null,
#     "unit_price": 109.99,
#     "price_with_tax": 136.3876,
#     "inventory": 23,
#     "collection": 2
# }
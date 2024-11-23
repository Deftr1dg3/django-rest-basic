from django.urls import path, include
# Use to build routs to ViewSets. DefaultRouter shows avaliable endpoints
# from rest_framework.routers import SimpleRouter, DefaultRouter
# For nested routers 

# Thirt party library for nested routing 'pip install drf-nested-routers'
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter() # type: ignore

router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='order')

# lookup='product' - prefix for parameter 'product_pk
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')  
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# Product images endpoint
products_router.register('images', views.ProductImageViewSet, basename='product-images')


cart_item_rounter = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_item_rounter.register('items', views.CartItemViewSet, basename='cart-items')


# from pprint import pprint 

# pprint(products_router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(cart_item_rounter.urls))
]



# urlpatterns = [
#     path('products/', views.ProductList.as_view(), name='products'),
#     path('products/<int:pk>', views.ProductDetail.as_view(), name='product_details'),
#     path('collections/', views.CollactionList.as_view(), name='collections'),
#     path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail')
# ]

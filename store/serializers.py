from __future__ import annotations
from decimal import Decimal

from django.db.models import Count
from django.db import transaction
from rest_framework import serializers

from .models import Product, Collection, Review, Cart, CartItem
from .models import Customer,  Order, OrderItem, ProductImage

from .signals import order_created


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review 
        fields = ['id', 'date', 'name', 'description']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
        
    

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection 
        fields = ['id', 'title', 'products_count']
    
    # Use read only to make custom field not to be Required during 
    # object creation.
    products_count = serializers.IntegerField(read_only=True)     

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(allow_blank=True)
#     price = serializers.DecimalField(max_digits=16, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')

#     # Handle related fields ------------------------------------
#     # Return Primary Key
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all()
#     # )
#     # Returns String representation of the model defined in __str__ method
#     # collection = serializers.StringRelatedField()+

#     # Nested object
#     collection = CollectionSerializer()
#     # Using hiperlink to the related field 
#     # collection = serializers.HyperlinkedRelatedField(
#     #     queryset=Collection.objects.all(),
#     #     view_name='collection-detail'
#     # )
    
#     def calculate_price_with_tax(self, product: Product) -> Decimal:
#         return product.unit_price * Decimal(1.24)


# ANOTHER WAY 

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ['id', 'title', 'unit_price']
        

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        product_image = ProductImage.objects.create(product_id=product_id, **validated_data) # type: ignore
        return product_image
    
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'price_with_tax', 'inventory', 'collection', 'images']
    
    # price = serializers.DecimalField(max_digits=16, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    # collection = CollectionSerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    
    # Custom method
    def calculate_price_with_tax(self, product: Product) -> Decimal:
        '''Method accepts the Product instance and calculates
        price with tax using its "unit_price" field'''
        return product.unit_price * Decimal(1.24)
    
    # # Override data validation
    # def validate(self, data):
    #     ...
    
    # # We can also override the create method 
    # # Example
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     # custom change
    #     product.other = 'whatewer'
    #     product.save()
    #     return product
    
    # # Override Update 
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
    

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ['title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_cart_item_price')
    
    def get_total_cart_item_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart 
        fields = ['id', 'items', 'total_price']

    # Will not appear in POST frorm in DjangoRest UI
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_cart_total_price')
    
    # Name of the method should atart with get_ it is convention
    def get_cart_total_price(self, cart: Cart) -> int:
        total_price = 0
        for cart_item in cart.items.all(): # type: ignore
            total_price += cart_item.quantity * cart_item.product.unit_price
        return total_price
    

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem 
        fields = ['id', 'product_id', 'quantity']
    
    product_id = serializers.IntegerField()
    
    # All validation methids start from validate_ (Convention)
    # Otherwise will not work.
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id'] # type: ignore
        quantity = self.validated_data['quantity'] # type: ignore
        try:
            # Updating existing Item
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
        except CartItem.DoesNotExist:
            # Creating a new Item
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data) # type: ignore

        cart_item.save()
        self.instance = cart_item
        
        return self.instance
    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem 
        fields = ['quantity']
        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer 
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
        
    user_id = serializers.IntegerField(read_only=True)
   


    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity', 'total_price']
    
    product = SimpleProductSerializer()
    unit_price = serializers.SerializerMethodField(method_name='get_unit_price')
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_unit_price(self, order_item: OrderItem):
        return order_item.product.unit_price
    
    def get_total_price(self, order_item: OrderItem):
        return order_item.product.unit_price * order_item.quantity
    
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order 
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items', 'total_price']
    
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self, order: Order):
        total_price = 0 
        item: OrderItem
        for item in order.items.all(): # type: ignore
            total_price += item.quantity * item.product.unit_price
        return total_price    


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ['payment_status']
    
    

class CreateOrderSerializer(serializers.Serializer):
    
    cart_id = serializers.UUIDField()
    
    # Validate + Field name will be executed automatically on .is_valid() method
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('The cart with provided id does not exist.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id
        
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id'] # type: ignore
            user_id = self.context['user_id']
            
            customer = Customer.objects.get(user_id=user_id)
            order = Order.objects.create(customer=customer)
            
            cart_items =  CartItem.objects.select_related('product').filter(cart_id=cart_id)
            
            order_items = [
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        unit_price=item.product.unit_price
                ) for item in cart_items
            ]
            
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=cart_id).delete()
            
            # Signal created in store/signals/__init__.py
            # First attribute is the SENDER then **kwargs
            order_created.send_robust(self.__class__, order=order)
            
            return order
       


        
        
        
        
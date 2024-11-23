from decimal import Decimal

from django.contrib import admin
from config.settings import common
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator

from uuid6 import uuid7

from .validators import valiodate_file_size

# For qodo test only ---------------------
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'


# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # Django will create "product_set" field that will store a set of 
    # products the promotion is applied to.


class Collection(models.Model):
    
    class Meta:
        ordering = ['title']
        
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    
    class Meta:
        ordering = ['title']
        
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=16, 
        decimal_places=2,
        validators = [MinValueValidator(Decimal('0.01'))]
        )
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    # Auto fullfil datetime on every update, if you use auto_now_add=True, Django will store only the creation datetime.
    last_update = models.DateTimeField(auto_now=True)
    # FK
    # Can be used with arg: related_name='..' to set the name of the field in the related table.
    # otherwise Django will set the name of the field automatically. Default: <origin_field_name>_set
    # "set_promotion"
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    # FK Many To Many. Django will create maby to many table on its own
    promotion = models.ManyToManyField(Promotion, blank=True)
    
    def __str__(self):
        return f"{self.title}"
    

class ProductImage(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # Pillow required for models.ImageField validations
    image = models.ImageField(
        upload_to='store/images',
        validators=[valiodate_file_size]
        )
    
    # Validating file extension. Set allowd extensions.
    # image = models.FileField(
    #     upload_to='store/images',
    #     validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jepg'])]
    #     )
    
    

class Customer(models.Model):
    class Meta:
        # indexes = [
        #     models.Index(fields=['last_name', 'first_name'], name='idx_last_name_first_name')
        # ]
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]
    
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    # Choices is collectio of tuples with (stored_value, human_readable_variant)
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(common.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_id')
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    # 1. Create function to set in in ModelAdmin class as field
    # FOR: list_display = ['first_name', 'last_name', 'membership', 'total_orders']   
    # 2. Use admin.display decorator to make sorting by values in the column.
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name 
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    

class Order(models.Model):
    
    # Customer permission
    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]
        
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # FK
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
     

# One To One relationship 
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # Options on_delete: models.CASCADE, models.PROTECT , models.SET_DEFAULT, models.SET_NULL
    # One To One relationship
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    
    # One To Many relationship 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class CartItem(models.Model):
    class Meta:
        unique_together = [['cart', 'product']]
        
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    
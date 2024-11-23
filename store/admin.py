from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Q, F, Count
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse

from . import models
from tags.models import TaggedItem

# Filters 

class InventoryFilter(admin.SimpleListFilter):
    # What you see on the filter panel
    title = 'inventory'
    # Parameter name
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<50', 'Low'),
            ('>50', 'Hight')
        ]
    
    # I,plementation of filtering logic
    def queryset(self, request, queryset):
        if self.value() == '<50':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>50':
            return queryset.filter(inventory__gt=50)
          
          


# Register your models here.

# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.Product)
# use decorator instead of previous comented rows


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'products_count']
    search_fields = ['title']
    
    # Override parent class method
    # to get needed results
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            products_count = Count('products')
        )
        return queryset
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # url = reverse('admin:app_model_targetpage')
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               })
               )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, product_image: models.ProductImage):
        if product_image.image.name != '':
            return format_html(f'<img src="{product_image.image.url}" class="thumbnail" />')
        return ''
    
         
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # Creating new record
    # readonly_fields = ['', '']
    # fields = ['title', 'slug']
    exclude = ['promotion']
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection']
    
    # Actions
    actions = ['clear_inventory']
    # Define inline in the same app
    inlines = [ProductImageInline]
    # Display
    list_display = ['id', 'title', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    list_editable = ['unit_price', 'inventory']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    # To pull needed info in one request and avoid multiple SQL requests.
    list_select_related = ['collection']
    
    search_fields = ['title']
    # inlines = [TagInline]
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 50:
            return 'Low'
        return 'Enough'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )
    
    class Media:
        css = {
            'all': [
                'store/styles.css'
            ]
        }
    
        


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'first_name', 'last_name', 'membership', 'total_orders']    
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    # ordering implemented in metaclass of the model
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    autocomplete_fields = ['user']
    
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_orders=Count('order')
        )
        return queryset 
    
    @admin.display(ordering='total_orders')
    def total_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               })
               )
        return format_html('<a href="{}">{}</a>', url, customer.total_orders)
        

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem 
    autocomplete_fields = ['product']
    # Minimum and maximum items per order
    min_num = 1
    max_num = 10
    # Display default placeholders
    # extra = 0
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    
    list_display = ['id', 'placed_at', 'customer_full_name', 'total_order_price']
    list_per_page = 10
    list_select_related = ['customer'] 
    
    inlines = [OrderItemInline]
    
    def customer_full_name(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'
    
    # To optimize your OrderAdmin class and prevent 
    # Django from sending a distinct SQL query for every 
    # orderitem_set, you can annotate the total price 
    # directly in the queryset. This way, you calculate 
    # the total price for all orders in a single query, 
    # improving performance significantly.
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_price=Sum(
                F('orderitem__unit_price') * F('orderitem__quantity'),
                output_field=DecimalField()
            )
        )
        return queryset

    
    @admin.display(description='Total Price')
    def total_order_price(self, order):
        return order.total_price

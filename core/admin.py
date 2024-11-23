from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product
from store.admin import ProductImageInline
from .models import User
from django.contrib.contenttypes.admin import GenericTabularInline 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class  TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    # How many default fields appear on ADD page
    extra = 3 
   
   
class CustomProductAdmin(ProductAdmin):
    # To list One To Many options
    inlines = [TagInline, ProductImageInline] 

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
        
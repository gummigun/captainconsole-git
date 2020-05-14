from django.contrib import admin

# Register your models here.
from .models import ShoppingCart, CartItem
# Register your models here.

admin.site.register(ShoppingCart)
admin.site.register(CartItem)
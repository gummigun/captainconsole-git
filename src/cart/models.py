from django.db import models
from django.conf import settings
from products.models import Products

# Create your models here.
class ShoppingCart(models.Model):
    #items = models.ManyToManyField(CartItem, null=True, blank=True)
    session = models.CharField(max_length=100, primary_key=True)
    user = models.DecimalField(max_digits=100, decimal_places=0, default=-1)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.id
    
class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


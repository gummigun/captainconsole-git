from django.shortcuts import render
from cart.models import ShoppingCart


# Create your views here.
def index(request):
    context = {'cart': ShoppingCart.objects.all().order_by('name')}
    return render(request, 'cart/cart.html', context)
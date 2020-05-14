from django.shortcuts import render, HttpResponseRedirect
from cart.models import ShoppingCart, CartItem
from django.urls import reverse

from products.models import Products
# Create your views here.
def index(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = ShoppingCart.objects.get(id=the_id)
        context = {"cart": cart}
    else:
        empty_message = "Your cart is empty."
        context = {'empty': True, "empty_message": empty_message}
    return render(request, 'cart/cart.html', context)

def update_cart(request, product_id):
    request.session.set_expiry(120000)
    try:
        qty =request.GET.get('qty')
        update_qty = True
    except:
        qty = ''
        update_qty = False
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = ShoppingCart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = ShoppingCart.objects.get(id=the_id)

    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        pass
    except:
        pass
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        print("Created cart item")
    if update_qty and qty:
        if int(qty) == 0:
            cart_item.delete()
        else:
            cart_item.quantity = qty
            cart_item.save()
    else:
        pass
  #  if not cart_item in cart.items.all():
  #      cart.products.add(cart_item)
   # else:
   #     cart.products.remove(cart_item)

    new_total = 0.00
    for item in cart.cartitem_set.all():
        line_total = float(item.products.price) * item.quantity
        new_total += line_total
    request.session['cart_total'] = new_total
    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse("cart"))
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from cart.models import ShoppingCart, CartItem
from django.db.models import Sum

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


def update_cart(request, id):
    print('updating cart')
    request.session.set_expiry(120000)

    # Grab the request parameters for product id and quantity and validate them
    # Validate product id
    try:
        product = Products.objects.get(id=id)
        price = product.price
    except Exception as err:
        print(err)
        HttpResponse(status=404)

    # Product exists. Validate quantity
    try:
        qty = request.GET['quantity']
        try:
            qty = int(qty)
        except ValueError:
            HttpResponse(status=400)

        update_qty = True
    except Exception as err:
        print(err)
        qty = ''
        update_qty = False

    # Get the user ID
    user_id = request.user.id
    if user_id is None:
        # User is not logged in.
        # Add item to the shopping cart without a user associated.
        user_id = -1

    # See if user already has an open cart
    cart = ShoppingCart.objects.get(session=request.session['cart_id'])

    # Create the cart item
    item = CartItem(cart=cart, products=product, quantity=qty, line_total=price)
    item.save()

    # Get the current cart total
    cart_total = {
        'total': CartItem.objects.filter(cart_id=cart).aggregate(Sum('line_total'))['line_total__sum'],
    }
    try:
        request.session['cart_total'] = float(
            CartItem.objects.filter(cart_id=request.session['cart_id']).aggregate(Sum('line_total'))['line_total__sum'])
    except TypeError:
        request.session['cart_total'] = 0.00
    return JsonResponse(cart_total, status=201)


def add_cart(request):
    # Check if 'add' is sent as a query parameter. Only add products if that is included.
    print(request.POST)
    if 'product' in request.POST:
        # Grab the product id and quantity from the post request
        pid = request.POST['product']
        qty = request.POST['quantity']

        # Get the current cart id
        try:
            cart = request.session['cart_id']
        except Exception as err:
            print(err)

        # Try to get the product
        try:

            product = Products.objects.get(id=pid)
            print(product.name)
            print(request.user.id)
        except:
            print('error')

        print(pid, qty)

    return HttpResponse(status=201)


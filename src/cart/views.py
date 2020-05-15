from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from cart.models import ShoppingCart, CartItem
from django.db.models import Sum

from django.urls import reverse

from products.models import Products
# Create your views here.
def index(request):


    print(request.session['cart_id'])
    # Get the cart id
    shopping_cart = ShoppingCart.objects.filter(session=request.session['cart_id'])
    print(shopping_cart)

    # Get the associated cart items
    i = CartItem.objects.filter(cart_id=request.session['cart_id']).values()
    print(i)

    items = [
        {
            'cart_id': x.cart.session,
            'product_id': x.products.id,
            'product_name': x.products.name,
            'price': x.products.price,
            'quantity': x.quantity,
            'subtotal': x.products.price * x.quantity,
        } for x in CartItem.objects.filter(cart_id=request.session['cart_id'])
    ]

    cart_total = 0
    for item in items:
        cart_total += item['subtotal']

    if not i:
        context = {'empty': True, "empty_message": 'empty_message'}
    else:
        context = {
            'total': "{:.2f}".format(cart_total),
            'products': items,
        }

    print(context)
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


def remove_cart(request, id):
    # Check if 'add' is sent as a query parameter. Only add products if that is included.
    print(request.GET)

    cart_id = request.GET['cart']
    print('removing', id, cart_id)

    item = CartItem.objects.filter(cart_id=cart_id, products_id=id).delete()
    print(item)

    if item[0] == 1:
        items = [
            {
                'cart_id': x.cart.session,
                'product_id': x.products.id,
                'product_name': x.products.name,
                'price': x.products.price,
                'quantity': x.quantity,
                'subtotal': x.products.price * x.quantity,
            } for x in CartItem.objects.filter(cart_id=request.session['cart_id'])
        ]

        cart_total = 0
        for item in items:
            cart_total += item['subtotal']

        context = {
                'total': "{:.2f}".format(cart_total),
                'products': items,
            }

        print(context)
        return render(request, 'cart/cart.html', context)


def checkout():
    # Get the cart info
    #

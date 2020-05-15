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

    try:
        request.session['cart_total'] = float(
            CartItem.objects.filter(cart_id=request.session['cart_id']).aggregate(total=Sum('line_total', field='line_total*quantity'))['total'])
    except TypeError:
        request.session['cart_total'] = 0.00

    context = {
        'cart_total': request.session['cart_total'],
        'items': items,
    }
    print(request.session['cart_total'])
    return JsonResponse(context, status=201)


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


def checkout(request):
    # Get the cart info
    # See if user already has an open cart
    item = CartItem.objects.filter(cart_id=request.session['cart_id'])
    print(item)

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
        'items': items,
        'total': cart_total,
    }
    return render(request, 'cart/checkout.html', context)


def review(request):
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
    return render(request, 'cart/review.html', context)


def process(request):
    print('POST REQUEST', request.POST)
    # Here we would add any logic to see if the payment is accepted

    # Assumes the payment is accepted.
    # Change the status of the current shopping cart to 2 (paid)
    curr_cart_id = request.session['cart_id']
    curr_cart = ShoppingCart.objects.filter(session=curr_cart_id)
    curr_cart.update(status=2)

    # Establish a new session for a new cart.
    new_session = request.session.create()

    fullname = request.POST['fullname']

    context = {
        'person': fullname,
    }
    return render(request, 'cart/thanks.html', context)
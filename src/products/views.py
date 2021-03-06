from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from products.models import Products, ProductImage, ProductCategories, ProductReview, ProductRating, SearchHistory
from cart.models import ShoppingCart, CartItem
from django.db.models import Sum, F

class DataContainer():
    def __init__(self):
        self.ORDER_BY = 'name'
        self.DATA = Products.objects.order_by(self.ORDER_BY)
        self.FILTERED = []
        self.CATEGORIES = 2
        self.CONSOLES = ''
        self.CONDITIONS = 3

    def set_data(self, data):
        self.DATA = data

    def get_data(self):
        return self.DATA

    def get_first(self):
        return self.FIRST_LOAD

    def set_order_by(self, val):
        self.ORDER_BY = val

    def get_order_by(self):
        return self.ORDER_BY

PRODUCTS = DataContainer()

def index(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('index')
    print('Fetching initial products data.')

    current_user = request.user.id
    if current_user is None:
        current_user = -1
    print(request.session.session_key)
    if not request.session.exists(request.session.session_key):
        request.session.create()

    try:
        cart = ShoppingCart.objects.get(session=request.session.session_key)
        request.session['cart_id'] = cart.session
        try:
            request.session['cart_total'] = float(CartItem.objects.filter(cart_id=request.session['cart_id']).aggregate(Sum('line_total'))['line_total__sum'])
        except TypeError:
            request.session['cart_total'] = 0.00
    except Exception:
        print('No active cart found. Creating a new cart.')
        new_cart = ShoppingCart(session=request.session.session_key, user=current_user)
        new_cart.save()
        request.session['cart_id'] = new_cart.session
        try:
            request.session['cart_total'] = float(CartItem.objects.filter(cart_id=request.session['cart_id']).aggregate(Sum('line_total'))['line_total__sum'])
        except TypeError:
            request.session['cart_total'] = 0.00

    print(request.session['cart_id'], request.session.session_key)

    # products = [
    #     {
    #         'id': x.id,
    #         'name': x.name,
    #         'category': x.category.name,
    #         'console': x.console,
    #         'manufacturer': x.manufacturer,
    #         'price': x.price,
    #         'shipping': x.shpping_code.code_name,
    #         'condition': x.condition.condition,
    #         'description': x.description,
    #         'firstImage': x.productimage_set.first().images,
    #         'allImages': list(x.productimage_set.values_list('images', flat=True)),
    #         'ratings': list(x.productrating_set.values_list('rating', flat=True)),
    #         'reviews': list(x.productreview_set.values_list('review', flat=True)),
    #     } for x in query
    # ]
    print('Fetching done.')

    if 'query' in request.GET:
        print('search')
        search_filter = request.GET['query']  # Grabs what's being filtered/searched
        if search_filter.lower() == 'video games':
            # Route to games
            games(request)
        elif search_filter.lower() == 'consoles':
            consoles(request)
        elif search_filter.lower() == 'accessories':
            accessories(request)
        elif search_filter.lower() == 'used':
            used(request)
        else:
            return search_query(request)
    elif 'filter' in request.GET:
        return filter_query(request)

    else:
        context = {
            'products': PRODUCTS.get_data(),
            'cart': request.session['cart_total'],
        }
        return render(request, 'index.html', context)


def products(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('products')

    print('Fetching search results.')
    if 'order' in request.GET:
        print('changing order')
        val = request.GET['order'].lower()
        print(val)
        PRODUCTS.set_order_by(val)
        return order_query(request)

    elif 'search' in request.GET:
        print('earch')
        query = request.GET['search']
        print(query)
        PRODUCTS.FILTERED = Products.objects.filter(name__icontains=query).order_by(PRODUCTS.get_order_by())
        print(PRODUCTS.FILTERED)
        print('Fetching done.')

        user = request.user.id
        if user is not None:
            # See if the search word exists for the user. Increment count if so. Else create the searchword in history.
            try:
                word = SearchHistory.objects.get(searchword=query)
                SearchHistory.objects.filter(user=user, searchword=query).update(count=F('count') + 1)
            except SearchHistory.DoesNotExist:
                searchword = SearchHistory(user=user, searchword=query.lower())
                searchword.save()


        context = {
            'products': PRODUCTS.FILTERED,
            'cart': request.session['cart_total'],
        }
        return render(request, 'products/products.html', context)
    elif 'filter' in request.GET:
        return filter_query(request)


def games(request):

    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    PRODUCTS.CATEGORIES = 2
    PRODUCTS.FILTERED = PRODUCTS.get_data().filter(category__exact=PRODUCTS.CATEGORIES).order_by(PRODUCTS.get_order_by())
    print(PRODUCTS.FILTERED)
    context = {
        'products': PRODUCTS.FILTERED,
        'cart': request.session['cart_total'],
    }
    return render(request, 'products/products.html', context)


def consoles(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    PRODUCTS.CATEGORIES = 1
    PRODUCTS.FILTERED = PRODUCTS.get_data().filter(category__exact=PRODUCTS.CATEGORIES).order_by(PRODUCTS.get_order_by())
    print(PRODUCTS.FILTERED)

    context = {
        'products': PRODUCTS.FILTERED,
        'cart': request.session['cart_total'],
    }
    return render(request, 'products/products.html', context)


def accessories(request):
    print(request.session['cart_id'], request.session.session_key)

    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    PRODUCTS.CATEGORIES = 3
    PRODUCTS.FILTERED = PRODUCTS.get_data().filter(category__exact=PRODUCTS.CATEGORIES).order_by(PRODUCTS.get_order_by())
    print(PRODUCTS.FILTERED)

    context = {
        'products': PRODUCTS.FILTERED,
        'cart': request.session['cart_total'],
    }
    return render(request, 'products/products.html', context)


def used(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    PRODUCTS.FILTERED = PRODUCTS.get_data().filter(condition__exact=2).order_by(PRODUCTS.get_order_by())
    context = {
        'products': PRODUCTS.FILTERED,
        'cart': request.session['cart_total'],
    }
    return render(request, 'products/products.html', context)


def search_query(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.

    # Define filtering capabilities here.
    if 'query' in request.GET:
        search_filter = request.GET['query']  # Grabs what's being filtered/searched

        user = request.user.id
        if user is not None:
            # See if the search word exists for the user. Increment count if so. Else create the searchword in history.
            try:
                word = SearchHistory.objects.get(searchword=search_filter.lower())
                SearchHistory.objects.filter(user=user, searchword=search_filter).update(count=F('count') + 1)
            except SearchHistory.DoesNotExist:
                searchword = SearchHistory(user=user, searchword=search_filter.lower())
                searchword.save()

        products = [
            {
                'id': x.id,
                'name': x.name,
                'category': x.category.name,
                'console': x.console,
                'manufacturer': x.manufacturer,
                'price': x.price,
                'shipping': x.shpping_code.code_name,
                'condition': x.condition.condition,
                'description': x.description,
                'firstImage': x.productimage_set.first().images,
            } for x in PRODUCTS.get_data().filter(name__icontains=search_filter.lower()).order_by(PRODUCTS.get_order_by())
        ]
        return JsonResponse({'data': products})


def filter_query(request):
    search_filter = request.GET['filter']  # Grabs the string after filter= in the request. Splits multiple checkboxes.
    filterby = request.GET['filterby']  # Grabs the string after filterby= in the request
    print('from get', search_filter, filterby)
    print(PRODUCTS.CATEGORIES, PRODUCTS.CONSOLES, PRODUCTS.CONDITIONS)
    print(PRODUCTS.FILTERED)
    if filterby == 'category':
        PRODUCTS.CATEGORIES = search_filter

    if filterby == 'console':
        PRODUCTS.CONSOLES = search_filter

    if filterby == 'condition':
        if search_filter == 'New':
            PRODUCTS.CONDITIONS = 1
        elif search_filter == 'Used':
            PRODUCTS.CONDITIONS = 2

    print('after', PRODUCTS.CATEGORIES, PRODUCTS.CONSOLES, PRODUCTS.CONDITIONS)
    print(PRODUCTS.FILTERED)

    products = [
        {
            'id': x.id,
            'name': x.name,
            'category': x.category.name,
            'console': x.console,
            'manufacturer': x.manufacturer,
            'price': x.price,
            'shipping': x.shpping_code.code_name,
            'condition': x.condition.condition,
            'description': x.description,
            'firstImage': x.productimage_set.first().images,
        } for x in PRODUCTS.get_data().filter(category__exact=PRODUCTS.CATEGORIES).filter(console__icontains=PRODUCTS.CONSOLES).filter(condition__lte=PRODUCTS.CONDITIONS).order_by(PRODUCTS.get_order_by())
    ]
    return JsonResponse({'data': products})

def order_query(request):
    search_filter = request.GET['order']  # Grabs the string after filter= in the request. Splits multiple checkboxes.
    products = [
        {
            'id': x.id,
            'name': x.name,
            'category': x.category.name,
            'console': x.console,
            'manufacturer': x.manufacturer,
            'price': x.price,
            'shipping': x.shpping_code.code_name,
            'condition': x.condition.condition,
            'description': x.description,
            'firstImage': x.productimage_set.first().images,
        } for x in PRODUCTS.get_data().filter(category__exact=PRODUCTS.CATEGORIES).filter(console__icontains=PRODUCTS.CONSOLES).filter(condition__lte=PRODUCTS.CONDITIONS).order_by(PRODUCTS.get_order_by())
    ]
    return JsonResponse({'data': products})


def history(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    user = request.user.id
    if user is not None:
        products = SearchHistory.objects.filter(user=user).order_by('-count')
        print(products)
        context = {
            'products': products,
        }
        return render(request, 'products/history.html', context)
    else:
        errormsg = 'You have to be logged in to see search history.'
        context = {
            'error': errormsg,
        }
        return render(request, 'products/history.html', context)


# /products/1
def get_product_by_id(request, id):
    return render(request, 'products/product_details.html', {
        'product': get_object_or_404(Products, pk=id),
        'cart': request.session['cart_total'],
    })

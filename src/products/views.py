from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from products.models import Products, ProductImage, ProductCategories, ProductReview, ProductRating


class DataContainer():
    def __init__(self):
        self.DATA = []
        self.FIRST_LOAD = True
        self.FILTERED = []

    def set_data(self, data):
        self.DATA = data

    def get_data(self):
        return self.DATA

    def get_first(self):
        return self.FIRST_LOAD

PRODUCTS = DataContainer()


def index(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('index')
    if PRODUCTS.get_first():
        print('Fetching initial products data.')
        query = Products.objects.order_by('category', 'name')
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
                'allImages': list(x.productimage_set.values_list('images', flat=True)),
                'ratings': list(x.productrating_set.values_list('rating', flat=True)),
                'reviews': list(x.productreview_set.values_list('review', flat=True)),
            } for x in query
        ]
        print('Fetching done.')
        PRODUCTS.set_data(products)
        print('Results', products)
        PRODUCTS.FIRST_LOAD = False

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
        }
        return render(request, 'index.html', context)


def games(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('video games')
    data = PRODUCTS.get_data()
    print(data)
    print('Starting filter')
    filtered = list(filter(lambda results: results['category'] == 'Video Games', data))
    print('Filter done')
    print(filtered)
    context = {
        'products': filtered,
    }
    return render(request, 'products/products.html', context)


def consoles(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('consoles')
    data = PRODUCTS.get_data()
    filtered = list(filter(lambda results: results['category'] == 'Consoles', data))
    print(filtered)
    context = {
        'products': filtered,
    }
    return render(request, 'products/products.html', context)


def accessories(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('accessories')
    data = PRODUCTS.get_data()
    filtered = list(filter(lambda results: results['category'] == 'Accessories', data))
    print(filtered)
    context = {
        'products': filtered,
    }
    return render(request, 'products/products.html', context)


def used(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('used')
    data = PRODUCTS.get_data()
    filtered = list(filter(lambda results: results['condition'] == 'Used', data))
    print(filtered)
    context = {
        'products': filtered,
    }
    return render(request, 'products/products.html', context)


def search_query(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.

    # Define filtering capabilities here.
    if 'query' in request.GET:
        search_filter = request.GET['query']  # Grabs what's being filtered/searched
        print(search_filter)
        data = PRODUCTS.get_data()
        filtered = list(filter(lambda results: search_filter.lower() in results['name'].lower(), data))
        print(filtered)
        return JsonResponse({'data': filtered})



def process_filter(filt_str):
    results = {
        'categories': '',
        'consoles': '',
        'condition': '',
    }
    print(filt_str)
    processed = filt_str.split('$')
    for item in processed:
        # Process categories selected
        if 'pc-' in item:
            # Product category prefix found
            item = item.replace('pc-', '')
            if '-' in item:
                item = item.replace('-', ' ')
            results['categories'] += item + '-'

        elif 'cond-' in item:
            item = item.replace('cond-', '')
            results['condition'] += item + '-'

        else:
            results['consoles'] += item + '-'

    print(results)
    return results



def filter_query(request):
    if 'filter' in request.GET:
        search_filter = request.GET['filter']  # Grabs the string after filter= in the request. Splits multiple checkboxes.
        filterby = request.GET['filterby']  # Grabs the string after filterby= in the request
        print(search_filter, filterby)

        processed = process_filter(search_filter)
        # Grab the data
        data = PRODUCTS.get_data()

        # Checking more than one checkbox within each filter category should expand the selection.
        # Checking more than one filter category should narrow the selection.

        filtered = []
        cons = []
        all_consoles = processed['consoles'].split('-')
        all_conditions = processed['condition'].split('-')

        print(all_consoles)
        if len(all_consoles) > 1:
            for c in all_consoles:
                if c != '':
                    cons += list(filter(lambda results: c.lower() in results['console'].lower(), data))
        else:
            cons = data

        print(cons)
        print(all_conditions)
        if len(all_conditions) > 1:
            for cond in all_conditions:
                if cond != '':
                    filtered += list(filter(lambda results: cond.lower() in results['condition'].lower(), cons))
        else:
            filtered = cons
        print(filtered)

        return JsonResponse({'data': filtered})


# /products/1
def get_product_by_id(request, id):
    return render(request, 'products/product_details.html', {
        'product': get_object_or_404(Products, pk=id)
    })

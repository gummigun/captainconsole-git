from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from products.models import Products, ProductImage, ProductCategories


def index(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('index')
    context = {
        'products': Products.objects.order_by('category', 'name'),
    }
    return render(request, 'index.html', context)


def games(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('video games')
    cat = [2]
    search_filter = ''
    cond = [1, 2]
    context = {
        'products': Products.objects.filter(category__in=cat).filter(name__icontains=search_filter).filter(condition__in=cond),
    }
    return render(request, 'products/products.html', context)


def consoles(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('consoles')
    cat = [1]
    search_filter = ''
    cond = [1, 2]
    context = {
        'products': Products.objects.filter(category__in=cat).filter(name__icontains=search_filter).filter(condition__in=cond),
    }
    return render(request, 'products/products.html', context)


def accessories(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('accessories')
    cat = [3]
    search_filter = ''
    cond = [1, 2]
    context = {
        'products': Products.objects.filter(category__in=cat).filter(name__icontains=search_filter).filter(condition__in=cond),
    }
    return render(request, 'products/products.html', context)


def used(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.
    print('used')
    cat = [1, 2, 3]
    search_filter = ''
    cond = [2]
    context = {
        'products': Products.objects.filter(category__in=cat).filter(name__icontains=search_filter).filter(condition__in=cond),
    }
    return render(request, 'products/products.html', context)


def search(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.

    # Define filtering capabilities here.
    if 'query' in request.GET:
        search_filter = request.GET['query']  # Grabs what's being filtered/searched
        print(search_filter)
        cat = [1, 2, 3]  # Id of all categories. Default search/filtering will use all three.
        cond = [1, 2]  # Id of all conditions. Default search/filtering will use both.

        if search_filter.lower() == 'consoles':
            cat = [1]
            search_filter = ''

        elif search_filter.lower() == 'video games':
            cat = [2]
            search_filter = ''
        elif search_filter.lower() == 'accessories':
            cat = [3]
            search_filter = ''
        elif search_filter.lower() == 'used':
            cond = [2]
            search_filter = ''

        # The products data container that is returned with the JsonResponse
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
            } for x in
            Products.objects.filter(category__in=cat).filter(name__icontains=search_filter).filter(condition__in=cond)
        ]
        print('search', products)
        return JsonResponse({'data': products})


# /products/1
def get_product_by_id(request, id):
    return render(request, 'products/product_details.html', {
        'product': get_object_or_404(Products, pk=id)
    })

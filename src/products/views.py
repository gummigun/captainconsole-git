from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from products.models import Products, ProductImage, ProductCategories


def index(request):
    # This function determines what is shown when the '/' or '/products/' indexes are requested.

    # Define filtering capabilities here.
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']  # Grabs what's being filtered/searched
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
            } for x in Products.objects.filter(category__in=cat).filter(name__icontains=search_filter).filter(condition__in=cond)
        ]
        return JsonResponse({'data': products})
    context = {
        'products': Products.objects.order_by('category', 'name'),
    }
    return render(request, 'products/products.html', context)


# /products/1
def get_product_by_id(request, id):
    return render(request, 'products/product_details.html', {
        'product': get_object_or_404(Products, pk=id)
    })

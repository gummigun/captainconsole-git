from django.shortcuts import render, get_object_or_404
from products.models import ProductsTest


def index(request):
    context = {'products': ProductsTest.objects.all().order_by('name')}
    return render(request, 'products/products.html', context)

# /products/1
def get_product_by_id(request, id):
    return render(request, 'products/product_details.html', {
        'product': get_object_or_404(ProductsTest, pk=id)
    })

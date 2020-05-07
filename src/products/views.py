from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from products.models import Products, ProductImage, ProductCategories


def index(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
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
            } for x in Products.objects.filter(name__icontains=search_filter)
        ]
        return JsonResponse({'data': products})
    context = {
        'products': Products.objects.all().order_by('name'),
    }
    return render(request, 'products/products.html', context)
    # name = models.CharField(max_length=255)
    # category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    # console = models.CharField(max_length=255)
    # manufacturer = models.CharField(max_length=255)
    # price = models.FloatField()
    # shpping_code = models.ForeignKey(ShippingCodes, on_delete=models.CASCADE)
    # condition = models.ForeignKey(ConditionCodes, on_delete=models.CASCADE)
    # description = models.CharField(max_length=4999, blank=True)

# /products/1
def get_product_by_id(request, id):
    return render(request, 'products/product_details.html', {
        'product': get_object_or_404(Products, pk=id)
    })

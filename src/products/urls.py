from django.urls import path
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="products"),
    path('<int:id>', views.get_product_by_id, name="product_details"),
]

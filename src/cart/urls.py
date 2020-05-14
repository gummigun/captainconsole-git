from django.urls import path, include
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="cart"),
    path('<int:id>', views.update_cart, name="update_cart"),
]
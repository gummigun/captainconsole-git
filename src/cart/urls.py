from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="cart"),
    path('<int:id>', views.update_cart, name="update_cart"),
    re_path(r'^add/$', views.add_cart, name="add_cart"),

]
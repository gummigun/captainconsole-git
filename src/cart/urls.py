from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="cart"),
    path('add/<int:id>', views.update_cart, name="update_cart"),
    path('remove/<int:id>', views.remove_cart, name="remove_cart"),
    path('review/', views.review, name="review"),
    path('checkout/', views.checkout, name="checkout"),
    path('process/', views.process, name="process")

    #re_path(r'^add/[0-9]$', views.update_cart, name="update_cart"),

]
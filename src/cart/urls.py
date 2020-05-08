from django.urls import path, include
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="cart"),
]
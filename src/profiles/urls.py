from django.urls import path, include
from . import views

urlpatterns = [
    # Home page url pattern
    path('profiles/<int:id>', views.get_profile_by_id, name="profile_details"),
    path('register', views.register ,name="register"),
    path('my-account', views.my_account, name="my_account"),
    path('login', include('django.contrib.auth.urls')),
    path('', include('django.contrib.auth.urls')),
]
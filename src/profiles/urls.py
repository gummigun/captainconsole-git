from django.urls import path, include
from . import views

urlpatterns = [
    # Home page url pattern
    path('profiles', views.index, name="profiles"),
    path('profiles/<int:id>', views.get_profile_by_id, name="profile_details"),
    path('register', views.register ,name="register"),
    path('login', views.login, name="login"),
    path('', include("django.contrib.auth.urls")),
]
from django.urls import path, include
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="profiles"),
    path('<int:id>', views.get_profile_by_id, name="profile_details"),
    path('register', views.register ,name="register"),
    path('', include("django.contrib.auth.urls")),
]
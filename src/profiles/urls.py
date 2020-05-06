from django.urls import path
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="profiles"),
    path('<int:id>', views.get_profile_by_id, name="profile_details"),
]
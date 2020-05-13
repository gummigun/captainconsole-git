from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Home page url pattern
    path('', views.index, name="index"),
    re_path(r'^video_games/$', views.games, name="games"),
    re_path(r'^consoles/$', views.consoles, name="consoles"),
    re_path(r'^accessories/$', views.accessories, name="accessories"),
    re_path(r'^used/$', views.used, name="used"),
    path('<int:id>', views.get_product_by_id, name="product_details"),
    path('search/', views.search, name="search"),
    path('', include('django.contrib.auth.urls')),
]

from django.urls import path, include
from base.views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us/', about, name='about-us'),
    path('login', login, name='login'),
    path('logout', logout_view, name='logout'),
    path('', include('subcategory.urls')),
    path('', include('category.urls')),
    # path('', include('products.urls')),
]



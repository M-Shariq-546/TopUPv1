from django.urls import path, include
from base.views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us/', about, name='about-us'),
    path('login', login, name='login'),
    path('logout', logout_view, name='logout'),
    path('', include('subcategory.urls')),
    path('register', register, name='register'),
    path('', include('category.urls')),
    path('reset-password', reset_password, name='reset_password_sending'),
    path('reset-password-confirm/', reset_password_confirm, name='reset-password-confirm'),
    # path('', include('products.urls')),
]



from django.urls import path, include
from .views import *

urlpatterns = [
    path('products/<str:subcategory_id>/', products_list, name='products-list'),
    path('product/<str:product_id>/', product_details, name='product_detail'),
]
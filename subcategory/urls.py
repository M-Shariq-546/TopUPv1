from django.urls import path
from .views import *
urlpatterns = [
    path('sub-categories/<str:id>/' , subcategories_list, name='subcategory_list')
]

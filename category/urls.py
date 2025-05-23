from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', categories, name='categories'),
    path('child_categories/<str:category>/', child_categories, name='child-categories'),
]

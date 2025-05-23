from django.shortcuts import render
from category.models import Category

def categories(request):
    return render(request, 'base/categories')


def child_categories(request, category):
    context = {}
    context['child_categories'] = Category.objects.filter(parent_category=category)

    return render(request, 'base/child_category.html', context)
from django.shortcuts import render
from .models import Products
from category.models import Category

def products_list(request, subcategory_id):
    context = {}
    products = Products.objects.filter(subcategory_id=subcategory_id)
    context['products_list'] = products
    context['categories'] = Category.objects.all()
    return render(request, 'base/products.html', context)

def product_details(request, product_id):
    context = {}
    product = Products.objects.get(id=product_id)
    context['product'] = product
    context['categories'] = Category.objects.all()
    return render(request, 'base/product_detail.html', context)
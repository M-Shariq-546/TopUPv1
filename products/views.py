from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from .models import Products, CartItem
from category.models import Category
from django.contrib import messages
from django.db import transaction

def products_list(request, subcategory_id):
    context = {}
    products = Products.objects.filter(subcategory_id=subcategory_id)
    context['products_list'] = products
    context['categories'] = Category.objects.all()
    return render(request, 'base/products.html', context)

def product_details(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    product = Products.objects.get(id=product_id)
    context['product'] = product
    context['categories'] = Category.objects.all()
    return render(request, 'base/product_detail.html', context)

def add_to_cart(request, product_id):
    with transaction.atomic():
        print('---- inside the cart view -----')
        product = get_object_or_404(Products, id=product_id)
        print('===== product found is ', product)
        if request.user.is_authenticated:
            print('====== authenticated user is ', request.user.is_authenticated)
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 1}
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            cart_item, created = CartItem.objects.get_or_create(
                session_key=request.session.session_key,
                product=product,
                defaults={'quantity': 1}
            )
            

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
    
from django.shortcuts import render, redirect
from category.models import Category
from subcategory.models import SubCategory
from django.contrib import messages 


def subcategories_list(request, id):
    context = {}
    if request.user.is_authenticated:
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(id=id)
        context['subcategories'] = SubCategory.objects.filter(category_id=id)
    else:
        messages.error(request, 'please login to get subcategories')
        return redirect('login')
    return render(request, 'base/subcategories.html', context)

from django.shortcuts import render, redirect
from auth_users_login.models import User
from django.contrib import messages 
from django.contrib.auth import logout
from category.models import Category
from subcategory.models import SubCategory
from products.models import Products
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
def home(request):
    context = {}
    context['categories'] = Category.objects.filter(parent_category__isnull=True)
    
    return render(request, 'base/home.html', context)

def about(request):
    return render(request, 'base/about.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if not email:
            messages.error(request, "Email is a required field.")
            return redirect('login')

        if not phone:
            messages.error(request, "Phone is a required field.")
            return redirect('login')
        
        if not password:
            messages.error(request, "Password is a required field.")
            return redirect('login')

        try:
            user = User.objects.get(email=email, phone=phone)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or phone number.")
            return redirect('login')

        if check_password(password, user.password):  # Only if password is hashed
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Replace 'home' with your home page URL name
        else:
            messages.error(request, "Incorrect password.")
            return redirect('login')
    return render(request, 'base/login.html')


def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'Successfully Logged out')
        return redirect('home')
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('home')
import os
import datetime
from django.shortcuts import render, redirect
from auth_users_login.models import User
from django.contrib import messages 
from django.contrib.auth import logout
from category.models import Category
from subcategory.models import SubCategory
from products.models import Products
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail

signer = TimestampSigner()

RESET_PASSWORD_TOKEN_EXPIRY_TIME = int(settings.RESET_PASSWORD_TOKEN_EXPIRY_TIME)


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

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already exists')
            return redirect('sign-up')
        
        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'This phone number is already in use')
            return redirect('sign-up')
        
        user = User.objects.create(
            email=email, 
            phone=phone,
        )

        if password:
            user.set_password(password)
        user.save() 

        auth_login(request, user)

        messages.success(request, "User Registered Successfully")
        return redirect('home')
    return render(request, 'base/register.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print('===== email ', email)
        try:
            user = User.objects.get(email=email)
            print('===== inside try user ', user)
        except User.DoesNotExist:
            messages.error(request, 'Email is not associated with any account')
            return redirect('login')

        # Create token with email and sign it
        signed_token = signer.sign(email)
        print('=-====== signed_token', signed_token)
        reset_url = request.build_absolute_uri(
            reverse('reset-password-confirm') + f'?token={signed_token}'
        )

        print('Email from settings ', settings.EMAIL_HOST_USER)
        print('Email from env ', os.environ.get('EMAIL_USER'))
        # Send the email
        send_mail(
            'Reset Your Password',
            f'Click the link below to reset your password:\n\n{reset_url}',
            os.environ.get('EMAIL_USER'),
            [email],
            fail_silently=False,
        )

        messages.success(request, 'Password reset link sent to your email.')
        return redirect('login')

def reset_password_confirm(request):
    token = request.GET.get('token')
    print('===== token ', token )
    if not token:
        messages.error(request, 'Invalid or missing token.')
        return redirect('login')

    try:
        email = signer.unsign(token, max_age=RESET_PASSWORD_TOKEN_EXPIRY_TIME * 3600)
        print('==== email ', email)
    except SignatureExpired as e:
        print('====== Signature expired error ', e)
        messages.error(request, 'The reset link has expired.')
        return redirect('login')
    except BadSignature as err:
        print('==== Bad signature error ', err)
        messages.error(request, 'Invalid reset token.')
        return redirect('login')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('password2')

        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        else:
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('login')

    return render(request, 'base/reset_password_confirm.html', {'token': token})
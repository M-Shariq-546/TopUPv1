from django.db import models
import uuid
from category.models import Category
from subcategory.models import SubCategory
from django.utils import timezone
from auth_users_login.models import User

class Products(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='product_sub_category')
    price = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() - self.added_at > timezone.timedelta(minutes=3)

    def __str__(self):
        return f"{self.product} and {self.quantity}"

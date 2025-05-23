from django.db import models
import uuid


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/category', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parent_category_key')

    def __str__(self):
        return self.name
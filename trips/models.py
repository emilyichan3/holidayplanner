from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static
from django_countries.fields import CountryField

User = get_user_model()
    
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    marker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marker')
     
    def __str__(self):
        return f'category: { self.category_name }'


class Plan(models.Model):
    plan_name = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    link = models.TextField(null=True, blank=True)
    country = CountryField(blank_label="(select country)", null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    planner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planner')
    categories = models.ManyToManyField(Category, related_name="plans")  # Many-to-Many relationship
    
    def __str__(self):
        return f'{ self.plan_name } is in { self.country }'
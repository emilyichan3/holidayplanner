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
    category_name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    marker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marker')
     
    def __str__(self):
        return f'category: { self.category_name }'

    def get_absolute_url(self):
        return reverse('trips-myCategory', kwargs={'user_id': self.marker.id})
        

class Plan(models.Model):
    plan_name = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    link = models.CharField(max_length=2000, null=True, blank=True)
    country = CountryField(blank_label="(select country)", null=True, blank=True)
    city = models.CharField(max_length=80,blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    planner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planner')
    categories = models.ManyToManyField(Category, related_name="plans")  # Many-to-Many relationship
    
    def __str__(self):
        return f'{ self.plan_name } is in { self.country }'


class Trip(models.Model):
    trip_name = models.CharField(max_length=200)
    trip_description = models.TextField(blank=True)
    date_fm = models.DateTimeField(default=timezone.now)
    date_to = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip')
    
    def __str__(self):
        return f'{ self.trip_name } is in { self.country }'


class Schedule(models.Model):
    destination = models.CharField(max_length=200)
    country = CountryField(blank_label="(select country)", null=True, blank=True)
    city = models.CharField(max_length=80,blank=True)
    date_visited = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=2000, null=True,  blank=True)
    note = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='trip_pics', storage=MediaCloudinaryStorage(), null=True, blank=True)
    attachement = models.FileField(upload_to='trip_files', storage=MediaCloudinaryStorage(), null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='schedule')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, related_name='visited', null=True, blank=True)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule')
    
    def __str__(self):
        return f'{ self.destination } is in { self.country }'

    def get_image_url(self):
        if self.image: # Generate a Cloudinary thumbnail URL
            return cloudinary_url(
                self.image.name, width=300, height=300, crop="lfill"
            )[0]
        else: # Fallback to static default image
            return static('trip/trip_default.jpg')
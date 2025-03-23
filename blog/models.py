from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static
from django_countries.fields import CountryField

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    country = CountryField(blank_label="(select country)", null=True, blank=True)
    city = models.CharField(max_length=80,blank=True)    
    image = models.ImageField(upload_to='blog_pics', storage=MediaCloudinaryStorage(), null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{ self.title } is written by { self.author.username }'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_image_url(self):
        if self.image: # Generate a Cloudinary thumbnail URL
            return cloudinary_url(
                self.image.name, width=300, height=300, crop="lfill"
            )[0]
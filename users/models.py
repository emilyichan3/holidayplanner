from django.db import models
# from PIL import Image # Change here from pillow import Image
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

class Profile(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150,blank=True)
    last_name = models.CharField(_("last name"), max_length=150,blank=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    # below code is for storing images locally.
    # image = models.ImageField(default='user_default.jpg', upload_to='profile_pics')
    # below code is for stroing images on https://cloudinary.com/home
    image = models.ImageField(upload_to='profile_pics', storage=MediaCloudinaryStorage(), null=True, blank=True)
    dob = models.DateField(default=datetime.utcnow)
    
    def __str__(self):
        return self.email
    # below code is for storing images locally by pillow.
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     with Image.open(self.get_image_url) as img:
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.get_image_url)

    def get_image_url(self):
        if self.image: # Generate a Cloudinary thumbnail URL
            return cloudinary_url(
                self.image.name, width=300, height=300, crop="lfill"
            )[0]
        else: # Fallback to static default image
            return static('users/user_default.jpg')
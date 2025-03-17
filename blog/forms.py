from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import URLValidator
from django_countries.fields import CountryField

class PostForm(forms.ModelForm):
    country = CountryField(blank_label="(select country)", 
                        null=True, blank=True)
    city = forms.CharField(max_length=80, 
                        label="Destination City",  # Ensure this line is included
                        required=False)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'clearable': 'true'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'country', 'city','image' ]



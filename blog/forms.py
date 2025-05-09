from django import forms
from django.contrib.auth import get_user_model
from .models import Post
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import URLValidator
from django_countries.fields import CountryField
from trips.models import Category, Plan
from django_countries.widgets import CountrySelectWidget

class PostForm(forms.ModelForm):
    country = CountryField(blank_label="(select country)", 
                        null=True, blank=True)
    city = forms.CharField(max_length=80, 
                        label="Destination City",  # Ensure this line is included
                        required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'country', 'city']


class PostConvertCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),  # Set dynamically in __init__
        widget=forms.CheckboxSelectMultiple,  # This allows users to select multiple categories
        required=True
    )
    link = forms.URLField(
        required=False,
        label='Enter a URL',
        validators=[URLValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com'})
    )
    country = CountryField().formfield(required=False, label="Country",
        widget=CountrySelectWidget()
    )    
    city = forms.CharField(max_length=80, required=False)

    class Meta:
        model = Plan
        fields = ['plan_name', 'link', 'country', 'city','categories', 'note' ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract menu instance
        post = kwargs.pop('post', None)  
        post_url = kwargs.pop('post_url', None)  
        super().__init__(*args, **kwargs)
        
        print(f"PlanForm initialized with user: {user}")  # Debugging output
        if user:
            self.fields['categories'].queryset = Category.objects.filter(marker=user)

        if post:
            self.fields['plan_name'].initial = post.title
            self.fields['country'].initial = post.country
            self.fields['city'].initial = post.city
            self.fields['link'].initial = post_url
            
            
            
  



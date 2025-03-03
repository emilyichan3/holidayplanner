from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


User = get_user_model()
# xxx/admin/
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("email","first_name", "last_name",'image','dob')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ("email","first_name", "last_name",'image','dob')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField(label="Date of Birth",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = Profile
        fields = ['email', "first_name", "last_name", 'password1', 'password2', 'dob']

    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob and dob > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        return dob


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField(required=False, 
                          widget=forms.DateInput(attrs={'type': 'date'}),
                          label="Date of Birth")
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'clearable': 'true'}))

    class Meta:
        model = Profile
        fields = ["first_name", "last_name",'image', 'dob']

    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob and dob > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        return dob


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm  #Import added
# for django 5, need to import logout
from django.contrib.auth import logout

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile #We want to import Profile from our models as we we will be creating a new profile
from django.contrib.auth.models import User #The user model will be the sender
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Create your views here.
def register(request):
    if request.method == 'POST':      
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('email')

            messages.success(request, f'Account created successfully, now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required # Added decorator here
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user)
        if  p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated') #Changes here
            return redirect('profile') #Changes here
        else:
            messages.error(request, 'Please correct the errors below.')  # Show an error message
    else:
        p_form = ProfileUpdateForm(instance=request.user)

    context = {
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context) #Context passed here

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html', {})
    

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = Profile
        fields = ("email","first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ("email", "first_name", "last_name")
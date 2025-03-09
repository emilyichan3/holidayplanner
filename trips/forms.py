from django import forms
from django.contrib.auth import get_user_model
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from .models import Plan, Category, Trip, Schedule
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class PlanForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows users to select multiple categories
        required=True
    )

    class Meta:
        model = Plan
        fields = ['plan_name', 'note', 'link', 'country', 'categories']


class myTripCreateForm(forms.ModelForm):
    trip_name = forms.CharField(max_length=200)
    trip_description = forms.CharField(max_length=500)
    date_fm = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Trip
        fields = ['trip_name', 
                'trip_description',
                'date_fm',
                'date_to']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # Only set default for new forms, not existing ones
            self.fields['date_fm'].initial = date.today()
            self.fields['date_to'].initial = date.today() + timedelta(days=7)  

    def clean(self):
        cleaned_data = super().clean()
        date_fm = cleaned_data.get("date_fm")
        date_to = cleaned_data.get("date_to")

        if date_fm and date_to:
            if date_to < date_fm:
                raise ValidationError("The end date must be later than the travel from date.")

        if date_to:
            if date_to < date.today():
                raise ValidationError("The end date must be today or a future date.")

        return cleaned_data
        

class myScheduleCreateForm(forms.ModelForm):
    trip_name = forms.CharField(max_length=200)
    date_fm = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    destination = forms.CharField(max_length=200)
    date_visited = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Schedule
        fields = ['trip_name',
                'date_fm',
                'date_to',
                'destination', 
                'date_visited']
        
    def __init__(self, *args, **kwargs):
        trip = kwargs.pop('trip', None)  # Extract trip instance
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # Only set default for new forms, not existing ones
            self.fields['date_visited'].initial = date.today()

        if trip:
            self.fields['trip_name'].initial = trip.trip_name  
            self.fields['date_fm'].initial = trip.date_fm 
            self.fields['date_to'].initial = trip.date_to 
            
            # Make fields read-only if they shouldn't be changed
            self.fields['trip_name'].widget.attrs['readonly'] = True
            self.fields['date_fm'].widget.attrs['readonly'] = True
            self.fields['date_to'].widget.attrs['readonly'] = True
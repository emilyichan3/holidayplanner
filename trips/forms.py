from django import forms
from django.contrib.auth import get_user_model
from .models import Plan, Category, Trip, Schedule
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import URLValidator

class PlanForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),  # Set dynamically in __init__
        widget=forms.CheckboxSelectMultiple,  # This allows users to select multiple categories
        required=True
    )
    link = forms.URLField(
        label='Enter a URL',
        validators=[URLValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract menu instance
        super().__init__(*args, **kwargs)
        print(f"PlanForm initialized with user: {user}")  # Debugging output
        if user:
            self.fields['categories'].queryset = Category.objects.filter(marker=user)

    class Meta:
        model = Plan
        fields = ['plan_name', 'link', 'country', 'city','categories', 'note' ]


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
    destination = forms.CharField(max_length=200)
    city = forms.CharField(max_length=80, required=False)
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    scheduled_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'clearable': 'true'}))
    link = forms.URLField(
        label='Enter a URL',
        validators=[URLValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com'}),
        required=False  # Make the field optional
    )

    class Meta:
        model = Schedule
        fields = ['destination', 
                'scheduled_date',
                'scheduled_time',
                'link',
                'country',
                'city',
                'image',
                'attachement']
        
    def __init__(self, *args, **kwargs):
        trip = kwargs.pop('trip', None)  # Extract trip instance
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # Only set default for new forms, not existing ones
            self.fields['scheduled_date'].initial = date.today()
            # self.fields['scheduled_time'].initial = datetime.now().replace(minute=0, second=0, microsecond=0).time()


        # if trip:
        #     self.fields['trip_name'].initial = trip.trip_name  
        #     self.fields['date_fm'].initial = trip.date_fm 
        #     self.fields['date_to'].initial = trip.date_to 
            
        #     # Make fields read-only if they shouldn't be changed
        #     self.fields['trip_name'].widget.attrs['readonly'] = True
        #     self.fields['date_fm'].widget.attrs['readonly'] = True
        #     self.fields['date_to'].widget.attrs['readonly'] = True

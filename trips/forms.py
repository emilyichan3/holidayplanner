from django import forms
from django.contrib.auth import get_user_model
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from .models import Plan, Category
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
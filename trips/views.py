from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.models import User #The user model will be the sender
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from .models import Plan, Category
from django.views import View
from .forms import PlanForm

User = get_user_model()

def home(request):
    return render(request, 'trips/home.html', {'title': 'Home'})


class CategoryListView(ListView):
    model = Category
    template_name = 'trips/home.html' # we can define the template either here or in the urls
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()  # Add all Plan objects to context
        return context


class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    template_name = 'trips/plan_form.html'
    fields = ['plan_name', 'note', 'link', 'country', 'categories']
    success_url = "/"  # You can change this to the desired success URL after form submission

    def form_valid(self, form):
        # Automatically assign the logged-in user as the planner when the form is valid
        form.instance.planner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Adding categories and plans to the context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Fetch all categories
        context['plans'] = Plan.objects.all()  # Fetch all plans
        return context


class PlansByCategoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Plan
    template_name = 'trips/myPlans.html'
    context_object_name = 'plans'

    def get_queryset(self):
        # Get the category_id from the URL kwargs
        category_id = self.kwargs.get('category_id')
        # Ensure the category exists
        category = get_object_or_404(Category, id=category_id)
        # Filter the Plan objects that are linked to this category
        plans = Plan.objects.filter(categories=category)
        return plans

    def test_func(self):
        category_id = self.kwargs.get('category_id') 
        category = get_object_or_404(Category, id=category_id)
        return self.request.user == category.marker  # Check if the logged-in user is the caterer
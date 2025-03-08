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
from django.views.generic import TemplateView

User = get_user_model()

class home(ListView):
    model = Category
    template_name = 'trips/home.html' # we can define the template either here or in the urls
    context_object_name = 'categories'


class MyCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'trips/myCategory_list.html' # we can define the template either here or in the urls
    context_object_name = 'categories'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        categories = Category.objects.filter(
            marker=user,
        )
        return categories
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()  # Add all Plan objects to context
        return context

    def test_func(self):
        return self.request.user.id == self.kwargs.get('user_id')
        

class MyCategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'trips/myCategory_form.html'
    fields = ['category_name', 'description']
    success_url = "/"

    def form_valid(self, form):
        form.instance.marker = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("trips-myCategory", kwargs={"user_id": user_id})


class MyCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    template_name = 'trips/myCategory_form.html'
    fields = ['category_name', 'description']

    def form_valid(self, form):
        form.instance.marker = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        category = self.get_object()
        return self.request.user == category.marker 


class MyCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'trips/myCategory_confirm_delete.html'

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("trips-myCategory", kwargs={"user_id": user_id})
    
    def test_func(self):
        category = self.get_object()
        return self.request.user == category.marker
    
    def form_valid(self, form):
        category = self.get_object()

        if category.plans.all().exists():  
            messages.error(self.request, "This category cannot be deleted because it has linked plans.")
            return redirect(reverse("trips-myCategory", kwargs={"user_id": category.marker.id}))
        return super().form_valid(form)  # Proceed with deletion if no menus exist


class MyPlanByCategoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Plan
    template_name = 'trips/myPlan_list.html'
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


class MyPlanListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Plan
    template_name = 'trips/myPlan_list.html' # we can define the template either here or in the urls
    context_object_name = 'plans'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        plans = Plan.objects.filter(
            planner=user,
        )
        return plans
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['plans'] = Plan.objects.all()  # Add all Plan objects to context
    #     return context

    def test_func(self):
        return self.request.user.id == self.kwargs.get('user_id')


class MyPlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    template_name = 'trips/myPlan_form.html'
    form_class = PlanForm
    success_url = "/"  # You can change this to the desired success URL after form submission

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("trips-myPlan", kwargs={"user_id": user_id})

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


class MyPlanUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Plan
    template_name = 'trips/myPlan_form.html'
    form_class = PlanForm

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("trips-myPlan", kwargs={"user_id": user_id})
    
    def test_func(self):
        plan = self.get_object()
        return self.request.user == plan.planner 


class MyPlanDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Plan
    template_name = 'trips/myPlan_confirm_delete.html'

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("trips-myPlan", kwargs={"user_id": user_id})

    def test_func(self):
        plan = self.get_object()
        return self.request.user == plan.planner 


class CalculatorView(TemplateView):
    template_name = 'trips/calculator.html' # we can define the template either here or in the urls
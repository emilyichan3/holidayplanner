from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import PostForm, PlanForm
from .models import Post
from trips.models import Category, Plan
from django import template


User = get_user_model()

class PostListView(ListView):
    register = template.Library()
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm    

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form) # Validate form by running form_valid method from parent class.


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm    

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form) # Validate form by running form_valid method from parent class.

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.order_by('-date_posted')


class PostConvertPlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    template_name = 'blog/post_add_myPlan_form.html'
    form_class = PlanForm

    def get_success_url(self):
        return reverse("blog-home")

    def get_form_kwargs(self):
        """Pass the logged-in user to the form dynamically."""
        kwargs = super().get_form_kwargs()
        print(f"User authenticated: {self.request.user.is_authenticated}")  # Debug auth status
        kwargs['user'] = self.request.user  # Ensure user is added
        return kwargs

    def form_valid(self, form):
        print(f"User authenticated: {self.request.user.is_authenticated}")  # Debug auth status
        # Automatically assign the logged-in user as the planner when the form is valid
        form.instance.planner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Adding categories and plans to the context
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username= self.request.user.username)
        categories = Category.objects.filter(
            marker=user,
        )
        context['categories'] = categories        
        plans = Plan.objects.filter(categories__in=categories)
        context['plans'] = plans
        return context

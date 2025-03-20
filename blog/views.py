from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpRequest
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from .forms import PostForm, PostConvertCreateForm
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
    form_class = PostConvertCreateForm

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs.get('pk')})

    def get_form_kwargs(self):
        # Pass instances to form
        kwargs = super().get_form_kwargs()
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        kwargs['post'] = post 
        kwargs['user'] = self.request.user  # Ensure user is added
        post_url = self.request.build_absolute_uri(reverse('post-detail', kwargs={'pk': post.pk}))
        kwargs['post_url'] = post_url
        print(post_url)        
        return kwargs

    def form_valid(self, form):
        # Automatically assign the logged-in user as the planner when the form is valid
        form.instance.planner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Adding post to template context
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        context['post'] = post
        return context

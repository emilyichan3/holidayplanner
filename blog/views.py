from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
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
from django.contrib import messages
from django.shortcuts import redirect

User = get_user_model()

class PostListView(ListView):
    register = template.Library()
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.order_by('-date_posted')        
            
        return posts

def Post_Search_Result(request):
    query = request.GET.get('q', '').strip()
    posts=[]
    total = 0
    paginate_by = 10

    if query:
        search_filter = ( 
                Q(country__icontains=query.strip()) | 
                Q(city__icontains=query.strip()) | 
                Q(title__icontains=query.strip()) | 
                Q(content__icontains=query.strip()))    
        posts = Post.objects.filter(search_filter).order_by('-date_posted')       
        total = posts.count()

    # Pagination
    paginator = Paginator(posts, paginate_by)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_search_result.html', {
        'posts': posts, 
        'query': query, 
        'total': total
    })


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
    template_name = 'blog/post_confirm_delete.html'
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = user.posts.order_by('-date_posted')

        return posts


def UserPost_Search_Result(request, username):
    user = get_object_or_404(User, username=username)
    query = request.GET.get('q', '').strip()
    username = user.username
    posts=[]
    total = 0
    paginate_by = 10

    if query:
        search_filter = ( 
                Q(author__id=user.id) & (
                Q(country__icontains=query.strip()) | 
                Q(city__icontains=query.strip()) | 
                Q(title__icontains=query.strip()) | 
                Q(content__icontains=query.strip())))    
        posts = Post.objects.filter(search_filter).order_by('-date_posted')       
        total = posts.count()

    # Pagination
    paginator = Paginator(posts, paginate_by)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/user_posts_search_result.html', {
        'posts': posts, 
        'query': query, 
        'total': total,
        'username':username
    })


class PostConvertPlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    template_name = 'blog/post_add_myPlan_form.html'
    form_class = PostConvertCreateForm

    def dispatch(self, request, *args, **kwargs):
        # dispatch() runs before get(), post(), etc.
        # Check if user has any categories
        user_categories = Category.objects.filter(marker=request.user)
        if not user_categories.exists():
            messages.warning(self.request, "You need to create a category before making a plan.")
            return redirect('trips-myCategory', username=request.user.username)  
        return super().dispatch(request, *args, **kwargs)

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
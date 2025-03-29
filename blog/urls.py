from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostConvertPlanCreateView,
    UserPostListView,
    Post_Search_Result,
    UserPost_Search_Result
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/search/', Post_Search_Result, name='post-search'),
    path('post/new/', PostCreateView.as_view(), name='post-new'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/user/<str:username>/search/', UserPost_Search_Result, name='user-posts-search'),
    path('post/<int:pk>/AssignToPlan/new/', PostConvertPlanCreateView.as_view(), name='post-Convert-myPlan-new'),
]

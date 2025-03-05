from django.urls import path
from .views import (
    CategoryListView,
    PlanCreateView,
    PlansByCategoryView
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", CategoryListView.as_view(), name='trips-home'),
    path("myCategories", CategoryListView.as_view(), name='trips-categories'),
    path('myPlans/', PlanCreateView.as_view(), name='trips-add-plan'),
    path('category/<int:category_id>/plans/', PlansByCategoryView.as_view(), name='plans-by-category'),
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 


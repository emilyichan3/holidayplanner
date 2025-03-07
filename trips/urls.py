from django.urls import path
from .views import (
    home,
    MyCategoryListView,
    MyCategoryCreateView,
    MyCategoryUpdateView,
    MyCategoryDeleteView,
    PlanCreateView,
    PlansByCategoryView,
    CalculatorView
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", home.as_view(), name='trips-home'),
    path("myCategory/<int:user_id>", MyCategoryListView.as_view(), name='trips-myCategory'),
    path("myCategory/new", MyCategoryCreateView.as_view(), name='trips-myCategory-new'),
    path('myCategory/<int:pk>/update/', MyCategoryUpdateView.as_view(), name='trips-myCategory-update'),
    path('myCategory/<int:pk>/delete/', MyCategoryDeleteView.as_view(), name='trips-myCategory-delete'),
    path('myPlan/', PlanCreateView.as_view(), name='trips-myPlan-new'),
    path('category/<int:category_id>/plans/', PlansByCategoryView.as_view(), name='trips-plans-by-category'),
    path("calculator/", CalculatorView.as_view(), name="calculator"),  # Use as_view()
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 


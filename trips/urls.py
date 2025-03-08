from django.urls import path
from .views import (
    home,
    MyCategoryListView,
    MyCategoryCreateView,
    MyCategoryUpdateView,
    MyCategoryDeleteView,
    MyPlanListView,
    MyPlanCreateView,
    MyPlanUpdateView,
    MyPlanDeleteView,
    MyPlanByCategoryView,
    CalculatorView
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", home.as_view(), name='trips-home'),
    path("myCategory/<int:user_id>", MyCategoryListView.as_view(), name='trips-myCategory'),
    path("myCategory/new", MyCategoryCreateView.as_view(), name='trips-myCategory-new'),
    path('myCategory/<int:pk>/update/', MyCategoryUpdateView.as_view(), name='trips-myCategory-update'),
    path('myCategory/<int:pk>/delete/', MyCategoryDeleteView.as_view(), name='trips-myCategory-delete'),
    path('myCategory/<int:category_id>/plans/', MyPlanByCategoryView.as_view(), name='trips-myPlans-by-myCategory'),
    path('myPlan/<int:user_id>', MyPlanListView.as_view(), name='trips-myPlan'),
    path('myPlan/new/', MyPlanCreateView.as_view(), name='trips-myPlan-new'),
    path('myPlan/<int:pk>/update/', MyPlanUpdateView.as_view(), name='trips-myPlan-update'),
    path('myPlan/<int:pk>/delete/', MyPlanDeleteView.as_view(), name='trips-myPlan-delete'),
    path("calculator/", CalculatorView.as_view(), name="calculator"),  # Use as_view()
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 


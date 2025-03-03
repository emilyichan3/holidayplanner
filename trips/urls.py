from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name='trips-home'),
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 


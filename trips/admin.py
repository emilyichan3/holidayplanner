from django.contrib import admin

# Register your models here.
from .models import Category, Plan, Trip, Schedule

admin.site.register(Category)
admin.site.register(Plan)
admin.site.register(Trip)
admin.site.register(Schedule)
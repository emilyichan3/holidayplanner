# admin.site.register(Profile)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Profile

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Profile
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active",'image','dob')
    list_filter = ("email", "first_name", "last_name", "is_staff", "is_active",'image','dob')
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("More",{"fields": ('image','dob')})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions",'image','dob',
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(Profile, CustomUserAdmin)
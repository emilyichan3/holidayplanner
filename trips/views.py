from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.models import User #The user model will be the sender
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError

User = get_user_model()

def home(request):
    return HttpResponse(b'<h1>Blog Home</h1>')

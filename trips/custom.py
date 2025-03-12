from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User #The user model will be the sender
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .models import Plan, Category, Trip, Schedule

def add_plan_to_mytrip(request, trip_id, plan_id):
    trip = get_object_or_404(Trip, id=trip_id)
    plan = get_object_or_404(Plan, id=plan_id)
    
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add a plan to your schedule.")
        return redirect('login') 

    user_id = request.user.id  # Ensure the user is authenticated

    # Create a new Schedule entry
    schedule = Schedule.objects.create(
        destination=plan.plan_name, 
        country=plan.country,
        city=plan.city,
        link=plan.link,
        note=plan.note,
        date_visited=trip.date_fm,
        trip=trip,  
        plan=plan,
        traveler=request.user  
    )

    return redirect(reverse("trips-mySchedule-Search", kwargs={"trip_id": trip_id, "user_id": user_id}))

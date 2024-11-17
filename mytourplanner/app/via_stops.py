from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib import messages

from app.models import ViaStops

# =====================================================
# Add Via Stops
# =====================================================
@login_required
def add_via_stops(request):
    if request.method == 'POST':
        return HttpResponse(1)
    return HttpResponse(2)


# =====================================================
# Update Via Stops
# =====================================================
@login_required
def edit_via_stops(request):
    if request.method == 'POST':
        return HttpResponse(1)
    return HttpResponse(2)


# =====================================================
# Delete Via Stops
# =====================================================
@login_required
def delete_via_stops(request):
    if request.method == 'POST':
        return HttpResponse(1)
    return HttpResponse(2)


# =====================================================
# Start Via Stop Time
# =====================================================
@login_required
def start_via_stop_time(request):
    if request.method == 'POST':
        return HttpResponse(1)
    return HttpResponse(2)


# =====================================================
# Stop Via Stop Time
# =====================================================
@login_required
def stop_via_stop_time(request):
    if request.method == 'POST':
        return HttpResponse(1)
    return HttpResponse(2)


# =====================================================
# Clear Via Start And Stop Time
# =====================================================

def clear_via_stop_time(request):
    if request.method == 'POST':
        return HttpResponse(1)
    return HttpResponse(2)
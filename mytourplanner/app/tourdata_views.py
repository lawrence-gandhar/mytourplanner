from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.forms.models import model_to_dict
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from app.models import TourData

from app.forms.tour_forms import (
    TourDataInitialForm,
    TourNextForm,
    TourDataUpdateForm
)

from app.forms.travelmode_forms import TravelModeCreateForm, TravelModeCostCreateForm

from app.modules.tour_counters import TourCounters as tc
from app.modules import db_operations as dbops
from app.modules import custom_constants as cs 

from datetime import datetime
import json

# =====================================================
# Update TourData
# =====================================================

@login_required(login_url="login")
def check_planned_date(request):
    if request.method == "GET":
        planned_date = request.GET.get("planned_to_start_on", None)
        planned_date = datetime.strptime(planned_date, "%Y-%m-%d")

        query = TourData.objects.filter(plan_to_start_on=planned_date).count()
        return HttpResponse(query)


# =====================================================
# Add TourData
# =====================================================
@login_required(login_url="login")
def add_tour(request):
    if request.method == "POST":
        form = TourDataInitialForm(request.POST)
        if form.is_valid():
            ins = form.save(commit=False)
            ins.user_id = request.session["user_id"]
            ins.save()

            msg = f'''Tour from <strong>{ins.source.upper()}</strong> to <strong>{ins.destination.upper()}</start> <br/>
            Planned to start on {ins.plan_to_start_on.strftime("%Y-%m-%d %H:%M")} is added Successfully.'''

            messages.add_message(request, messages.SUCCESS, msg)

        return redirect("tour_next_step", ins.pk)
    else:
        return HttpResponseNotFound("Method Not Allowed")


# =====================================================
# View for TourData Next Steps
# =====================================================
@login_required(login_url="login")
def tour_next_step(request, id=None):
    data = {}

    ins = dbops.get_tourdata(id)

    print(ins)

    if ins:

        tour_data = dbops.fetch_travelmode_data(tour_data_id=int(id))

        total_cost_adults = 0
        total_cost_children = 0
        total_gst = 0
        total_distance = 0

        for row in tour_data:
            total_cost_adults += row["no_of_adults"] * row["travelmode_cost__cost_per_adult"]
            total_cost_children += row["no_of_children"] * row["travelmode_cost__cost_per_child"]
            total_gst += row["gst"] 
            total_distance += row["distance"] 

        total_expenditure = total_cost_adults + total_cost_children + total_gst

        data.update({
            "tour_next_form":TourNextForm(instance=ins, prefix="tourdata"), 
            "ins": ins,
            "tour_data":tour_data,
            "total_cost_adults": total_cost_adults,
            "total_cost_children": total_cost_children,
            "total_gst": total_gst,
            "total_expenditure": total_expenditure,
            "total_distance": total_distance,
            "travel_class_type": json.dumps(cs.TRAVELMODE_CLASS_TYPE),
            "travel_mode_form": TravelModeCreateForm(prefix="travel_mode"),
            "travel_cost_form": TravelModeCostCreateForm(prefix="travel_cost")
        })
        return render(request, "tour_next_step.html", data)
    else:
        return HttpResponseNotFound()

# =====================================================
# Add/Update for TourData Next Steps
# =====================================================
@login_required(login_url="login")
def add_update_travel_date(request, id):
    user = request.session["user_id"]
    
    ins = dbops.get_tourdata(id)
    if ins:
        tour_next_form = TourNextForm(request.POST, prefix="tourdata")

        if tour_next_form.is_valid():
            travel_start_date = tour_next_form.cleaned_data["travel_start_date"]
            budget = tour_next_form.cleaned_data["budget"]

            ins.travel_start_date = travel_start_date
            ins.budget = budget
            ins.save()
    else:
        messages.ERROR(request, "Invalid operation performed.")
        return redirect("home")
    return redirect("tour_next_step", id)
        
        
# =====================================================
# Update TourData
# =====================================================
@login_required(login_url="login")
def update_tour(request):
    ins = TourData.objects.get(pk=request.GET["id"]).values_list()
    return JsonResponse(ins, safe=False)


# =====================================================
# End Tour
# =====================================================
@login_required(login_url="login")
def end_tour(request, id=None):
    try:
        ins = TourData.objects.get(pk=int(id), user_id=request.session["user_id"])
        ins.travel_end_date = datetime.now()
        ins.plan_to_start_on = None
        ins.save()
        messages.add_message(request, messages.SUCCESS, "Tour Ended")
    except:
        messages.ERROR(request, "Invalid operation performed")

    return redirect("tour_next_step", id)

# =====================================================
# Delete Tour
# =====================================================
@login_required(login_url="login")
def delete_tour(request, id=None):
    pass
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from app.modules import travelmode_db_operations as travelmode_dbops

from app.forms.travelmode_forms import TravelModeCreateForm, TravelModeCostCreateForm


# =====================================================
# Next Steps for TravelMode and TravelCost
# =====================================================
@login_required(login_url="login")
def add_travel_mode_cost(request, id):
    user_id = request.session["user_id"]

    travel_mode_form = TravelModeCreateForm(request.POST, prefix="travel_mode")
    travel_cost_form = TravelModeCostCreateForm(request.POST, prefix="travel_cost")

    if travel_mode_form.is_valid():
        travel_mode_ins = travel_mode_form.save(commit=False)
        travel_mode_ins.tour_id = int(id)
        travel_mode_ins.user_id = user_id
        travel_mode_ins.save()
    else:
        messages.error(request, f"Form submission failed. {travel_mode_form.errors}")
        return redirect("tour_next_step", id)
        
    if travel_cost_form.is_valid():
        travel_cost_ins = travel_cost_form.save(commit=False)
        travel_cost_ins.travel_mode_id = travel_mode_ins.id
        travel_cost_ins.save()
        messages.success(request, "Form submission is successful")
    else:
        travel_mode_ins.delete()
        messages.error(request, f"Form submission failed. {travel_cost_form.errors}")
    return redirect("tour_next_step", id)


# =====================================================
# Next Steps for TravelMode and TravelCost
# =====================================================
@login_required(login_url="login")
def get_travel_mode(request, tour_id):
    user_id = request.session["user_id"]

    obj =  dbops()

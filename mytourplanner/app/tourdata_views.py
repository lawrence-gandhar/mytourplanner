from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.forms.models import model_to_dict
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from app.models import TourData

from app.forms.tour_forms import (
    TourDataInitialForm,
    TourNextForm,
    TourDataUpdateForm
)

from app.modules.tour_counters import TourCounters as tc
from app.modules import db_operations as dbops 

from datetime import datetime


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
# Next Steps for TourData
# =====================================================
class TourNextStep(LoginRequiredMixin, View):

    def get(self, request, id):
        self._user_id = request.session["user_id"]
        self._data = {}

        ins = dbops.get_tourdata(id)
        if ins:
            self._data.update({
                "tour_next_form":TourNextForm(instance=ins, prefix="tourdata"), 
                "ins": ins
            })

            print(self._data)
        else:
            return redirect("home")

        return render(request, "tour_next_step.html", self._data)


    def post(self, request):
        self._user_id = request.session["user_id"]

        return HttpResponse(1)


# =====================================================
# Update TourData
# =====================================================
@login_required(login_url="login")
def update_tour(request):
    ins = TourData.objects.get(pk=request.GET["id"]).values_list()
    print(ins)
    return JsonResponse(ins, safe=False)


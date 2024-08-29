from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from datetime import datetime

from app.models import (
    TourData,
    TollData,
    ViaStops,
    StayData,
    StopsData
)

from app.modules.my_calendar import GetCalendar
from app.modules import db_operations as dbops
from app.modules import custom_decorators as cds
from app.modules import tour_counters as tc

from app.forms.tour_forms import (
    TourDataInitialForm,
    TourDataUpdateForm
)

# Create your views here.

# =====================================================
# Login
# =====================================================
class LoginView(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        username = request.POST["username"].strip()
        passwd = request.POST["passwd"].strip()

        if username and passwd:
            user = authenticate(request, username=username, password=passwd)

            if user:
                login(request, user)
                request.session["user_id"] = user.id
                return redirect("home")
        return HttpResponse(0)

# =====================================================
# Home Page
# =====================================================


def create_calendar(request):
    return render(request, "calendar.html")


@login_required(login_url="login")
def home(request):
    if request.method == "GET":
        user_id = request.session["user_id"]
        queryset = dbops.fetch_tourdata(user_id)
        calendar = GetCalendar(user_id, queryset)
        upcoming_tours= []
        unfinished_tours = []
        completed_tours = []
        today = datetime.strptime(datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d").date()

        planned_tours = dbops.fetch_planned_tours(queryset=queryset)

        tour_counters = tc.TourCounters(request.session["user_id"])

        for row in planned_tours:
            if row["plan_to_start_on"] < today or row["put_on_hold"]:
                unfinished_tours.append(row)
            elif row["plan_to_start_on"] > today:
                upcoming_tours.append(row)

        context = {
            "calendar": calendar.htmlcalendar(),
            "tour_plan_form": TourDataInitialForm(),
            "completed_tours": dbops.fetch_completed_tours(queryset=queryset),
            "upcoming_tours": upcoming_tours,
            "unfinished_tours": unfinished_tours,
            "current_date": today.strftime("%d %B, %Y")
        }
            
        return render(request, "home.html", context)
    else:
        return HttpResponseNotFound("Method Not Allowed") 



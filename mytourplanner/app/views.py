from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required

from datetime import datetime

from app.modules.my_calendar import GetCalendar
from app.modules import tourdata_db_operations as tourdata_dbops
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

@login_required(login_url="login")
def home(request):
    if request.method == "GET":
        user_id = request.session["user_id"]
        queryset = tourdata_dbops.fetch_tourdata(user_id)
        calendar = GetCalendar()
        upcoming_tours= []
        unfinished_tours = []
        on_going_tours = []
        cancelled_tours = []

        today = datetime.strptime(datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d").date()

        planned_tours = tourdata_dbops.fetch_planned_tours(queryset=queryset)

        tour_counters = tc.TourCounters(request.session["user_id"])

        for row in planned_tours:
            print(row)
            if (row["plan_to_start_on"] < today or row["put_on_hold"]) and not row["travel_start_date"]:
                unfinished_tours.append(row)
            if row["plan_to_start_on"] > today:
                upcoming_tours.append(row)
            if row["travel_start_date"] and not row["travel_end_date"]:
                on_going_tours.append(row) 
            if row["cancelled"]:
                cancelled_tours.append(row)


        context = {
            "calendar": calendar.htmlcalendar(user_id, queryset),
            "tour_plan_form": TourDataInitialForm(),
            "completed_tours": tourdata_dbops.fetch_completed_tours(queryset=queryset),
            "upcoming_tours": upcoming_tours,
            "unfinished_tours": unfinished_tours,
            "current_date": today.strftime("%d %B, %Y"),
            "tour_counters": tour_counters.process_data(),
            "on_going_tours": on_going_tours,
            "cancelled_tours": cancelled_tours
        }
            
        return render(request, "home.html", context)
    else:
        return HttpResponseNotFound("Method Not Allowed") 


@login_required(login_url="login")
def fetch_calendar(request):
    if request.method == "GET":
        user_id = request.session["user_id"]
        month = request.GET.get("month", None)
        year = request.GET.get("year", None)

        queryset = tourdata_dbops.fetch_tourdata(user_id)
        calendar = GetCalendar()
        return HttpResponse(calendar.htmlcalendar(user_id, queryset, month=int(month), year=int(year)))
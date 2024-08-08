from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
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

from app.app_forms import (
    TourDataInitialForm,
    TourDataUpdateForm
)

# mixin
class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

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
        calendar = GetCalendar(request.session["user_id"])

        completed_tours = TourData.objects.filter(
            user_id = request.session["user_id"], 
            travel_end_date__isnull = True
        ).reverse()[:5]

        upcoming_tours = TourData.objects.filter(
            user_id = request.session["user_id"], 
            travel_start_date__isnull = True,
            plan_to_start_on__gte = datetime.today().strftime("%Y-%m-%d")
        )


        data = {
            "calendar": calendar.htmlcalendar(),
            "tour_plan_form": TourDataInitialForm(),
            "completed_tours": completed_tours,
            "upcoming_tours": upcoming_tours
        }
            
        return render(request, "home.html", data)
    else:
        return HttpResponseNotFound("Method Not Allowed") 


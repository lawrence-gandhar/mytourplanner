from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required

from app.modules.my_calendar import GetCalendar

from app.app_forms import (
    TourDataInitialForm
)

# Create your views here.

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
                return redirect("home")
        return HttpResponse(0)


@login_required
def home(request):

    calendar = GetCalendar()
    data = {
        "calendar": calendar.htmlcalendar(),
        "tour_plan_form": TourDataInitialForm()
    }
    
    return render(request, "home.html", data)

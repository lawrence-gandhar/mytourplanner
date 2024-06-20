from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

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


@login_required
def update_tour(request):

    ins = model_to_dict(TourData.objects.get(pk=request.GET["id"]))

    print(ins)

    return JsonResponse(ins, safe=False)

import app.views as app_view
import app.tourdata_views as tour_view
from django.urls import path

# Home Views 
urlpatterns = [
    path("", app_view.LoginView.as_view(), name="login"),
    path("home/", app_view.home, name="home"),
]

# TourData Validators
urlpatterns +=[
    path("check_planned_date/", tour_view.check_planned_date, name="check_planned_date"),
]

# CRUD TourData
urlpatterns += [ 
    path("add_tour/", tour_view.add_tour, name="add_tour"),
    path("tour_next_step/<int:id>/", tour_view.TourNextStep.as_view(), name="tour_next_step"),
    path("update_tour/", tour_view.update_tour, name="update_tour"),
]

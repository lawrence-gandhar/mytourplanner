import app.views as app_view
import app.tourdata_views as tour_view
import app.tourdata_api_view as tour_api_view
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
    path("update_tour/", tour_view.update_tour, name="update_tour"),
]

# Tour Data APIs
urlpatterns += [
    path("tourdata_latest/", tour_api_view.tourdata_latest, name="tourdata_latest"),
    path("tourdata_planned/", tour_api_view.tourdata_planned, name="tourdata_planned")
]
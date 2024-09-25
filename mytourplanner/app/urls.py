import app.views as app_view
import app.tourdata_views as tour_view
import app.travelmode_view as travel_mode
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app.api import tours_api

# Home Views 
urlpatterns = [
    path("", app_view.LoginView.as_view(), name="login"),
    path("home/", app_view.home, name="home"),
    # path("logout/", )
]

# AJAX Calls
urlpatterns += [
    path("fetch_calendar/", app_view.fetch_calendar, name="fetch_calendar")
]


# API
urlpatterns += [
    path("api/planned-tours/", tours_api.ListPlannedTours.as_view(), name="planned_tours"),
]


# TourData Validators
urlpatterns +=[
    path("check_planned_date/", tour_view.check_planned_date, name="check_planned_date"),
]

# CRUD TourData
urlpatterns += [ 
    path("add_tour/", tour_view.add_tour, name="add_tour"),
    path("tour_next_step/<int:id>/", tour_view.tour_next_step, name="tour_next_step"),
    path("add_update_travel_date/<int:id>/", tour_view.add_update_travel_date, name="add_update_travel_date"),
    path("add_travel_mode_cost/<int:id>/", travel_mode.add_travel_mode_cost, name="add_travel_mode_cost"),
    path("update_tour/", tour_view.update_tour, name="update_tour"),
    path('end_tour/<int:id>/', tour_view.end_tour, name="end_tour"),
    path('delete_tour/<int:id>/', tour_view.delete_tour, name="delete_tour")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


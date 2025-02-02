import app.views as app_view
import app.tourdata_views as tour_view
import app.travelmode_view as travel_mode
import app.via_stops as via_stops
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app.api import tours_api

# Home Views 
urlpatterns = [
    path("", app_view.LoginView.as_view(), name="login"),
    path("home/", app_view.home, name="home"),
    # path("logout/", )
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
    path("update_tour/", tour_view.update_tour, name="update_tour"),
    path('end_tour/<int:id>/', tour_view.end_tour, name="end_tour"),
    path('delete_tour/<int:id>/', tour_view.delete_tour, name="delete_tour"),
    path('cancel_tour/<int:id>/', tour_view.cancel_tour, name="cancel_tour")
] 

# CRUD TravelMode
urlpatterns += [
    path("add_travel_mode_cost/<int:id>/", travel_mode.add_travel_mode_cost, name="add_travel_mode_cost"),
]


# CRUD ViaStops
urlpatterns += [
    path("add_via_stops/", via_stops.add_via_stops, name="add_via_stops"),
    path("edit_via_stops/<int:id>/", via_stops.edit_via_stops, name="edit_via_stops"),
    path("delete_via_stops/<int:id>/", via_stops.delete_via_stops, name="delete_via_stops"),
    path("start_via_stop_time/<int:id>/", via_stops.start_via_stop_time, name="start_via_stop_time"),
    path("stop_via_stop_time/<int:id>/", via_stops.stop_via_stop_time, name="stop_via_stop_time"),
    path("clear_via_stop_time/<int:id>/", via_stops.clear_via_stop_time, name="clear_via_stop_time"),
]



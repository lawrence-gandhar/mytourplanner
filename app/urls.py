import app.views as app_view
from django.urls import path

urlpatterns = [
    path("", app_view.LoginView.as_view()),
    path("home", app_view.home, name="home"),
    path("update_tour", app_view.update_tour, name="update_tour")
]

from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("menu/", views.menu_view, name="menu"),
    path("logout/", views.logout_view, name="logout"),
]
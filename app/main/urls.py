from django.urls import path
from . import views


urlpatterns = [
    path("", views.main, name="main"),
    path("<str:weapon>", views.weapon, name="weapon")
]
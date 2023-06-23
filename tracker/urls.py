from CelestialOT.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="index"),
    path("base", views.base, name="base"),
]

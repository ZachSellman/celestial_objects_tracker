from CelestialOT.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="index"),
    path("base", views.base, name="base"),
    path("leftbar", views.leftbar, name="leftbar"),
    path("rightbar", views.rightbar, name="rightbar"),
    path("nobar", views.nobar, name="nobar"),
]

from django.shortcuts import render

# Create your views here.


def homepage(request):
    return render(request, "tracker/index.html")


def base(request):
    return render(request, "tracker/base.html")


def leftbar(request):
    return render(request, "tracker/left-sidebar.html")


def rightbar(request):
    return render(request, "tracker/right-sidebar.html")


def nobar(request):
    return render(request, "tracker/no-sidebar.html")

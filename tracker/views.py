from django.shortcuts import render

# Create your views here.


def homepage(request):
    return render(request, "tracker/index.html")


def base(request):
    return render(request, "tracker/base.html")

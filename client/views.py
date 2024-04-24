from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Championship
# from football.models import Season, Competition


# Create your views here.
def home(request):
    context = {}
    return render(request, "main/home.html", context)


# Create your views here.
def about(request):
    context = {}
    return render(request, "main/about.html", context)


# Create your views here.
def events(request):
    context = {}
    return render(request, "main/Events.html", context)


# Create your views here.
def contact(request):
    context = {}
    return render(request, "main/Contact.html", context)


# Create your views here.
def championship(request, id):
    champy = get_object_or_404(Championship, id=id)
    context = {"champy": champy}
    return render(request, "football/championship.html", context)



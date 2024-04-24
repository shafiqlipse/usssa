from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Championship
from football.models import Season
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import *

# Create your views here.


def newSeason(request):
    context = {}
    return render(request, "", context)


def EditSeason(request, id):
    context = {}
    return render(request, "", context)


def SeasonDetail(request, id):
    context = {}
    return render(request, "", context)


def DeleteSeason(request, id):
    context = {}
    return render(request, "", context)


def disciplines(request):
    context = {}
    return render(request, "season/disciplines.html", context)


def newChampionship(request):
    if request.method == "POST":
        form = ChampionshipForm(request.POST, request.FILES)
        if form.is_valid():
            # Assuming you have a method check_unique_field in your form that performs the uniqueness check
            form.save()
            messages.success(request, "Championship created successfully.")
            return redirect("champs")  # Redirect to a success URL

        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = ChampionshipForm()

    context = {"form": form}
    return render(request, "championship/newchamp.html", context)


def Championshipdetail(request, id):
    championship = Championship.objects.get(id=id)
    seasons = Season.objects.filter(championship=championship)
    if request.method == "POST":
        cform = SeasonForm(request.POST, request.FILES)

        if cform.is_valid():
            season = cform.save(commit=False)
            season.championship = championship
            season.save()
            return HttpResponseRedirect(reverse("champ", args=[int(id)]))
    else:
        cform = SeasonForm()
    context = {"championship": championship, "cform": cform, "seasons": seasons}
    return render(request, "championship/champ.html", context)


def editChampionship(request, id):
    context = {}
    return render(request, "", context)


def DeleteChampionship(request, id):
    champ = get_object_or_404(Championship, pk=id)

    if request.method == "POST":
        champ.delete()
        return redirect("champs")  # Redirect to the team list page or another URL
    context = {"champ": champ}
    return render(request, "championship/deleteChamp.html", context)


def Championships(request):
    champs = Championship.objects.all()
    context = {"champs": champs}
    return render(request, "championship/champs.html", context)

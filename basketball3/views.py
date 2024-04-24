from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *

from .filters import *
from accounts.models import Sport
from django.http import JsonResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def basketball3(request):
    basketball3X3 = Sport.objects.get(id=12)
    comps = B3Competition.objects.filter(sport=basketball3X3)

    if request.method == "POST":
        cform = CompForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = basketball3X3
            competn.save()
            return HttpResponseRedirect(reverse("basketball3"))
    else:
        cform = CompForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "comps": comps}
    return render(request, "football/football.html", context)

# @school_required
def create_competition(request):
    competitions = B3Competition.objects.all()
    baketball3 = Sport.objects.filter(id=6).first()
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.sport = baketball3
            comp.save()

            return redirect("b3comps")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = CompForm()

    return render(request, "comps/newb3comp.html", {"form": form})


# template


# officials list, tuple or array
def competitions(request):
    
    myFilter = CompetitionFilter(request.GET, queryset=competitions)

    competitionlist = myFilter.qs

    items_per_page = 10

    paginator = Paginator(competitionlist, items_per_page)
    page = request.GET.get("page")

    try:
        competitionlist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        competitionlist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        competitionlist = paginator.page(paginator.num_pages)
    context = {"competitionlist": competitionlist, "myFilter": myFilter}
    return render(request, "basketball3/competitions.html", context)


# view official details
def competition_details(request, id):
    b3competition = B3Competition.objects.get(id=id)
  
    context = {"b3competition": b3competition}
    return render(request, "comps/b3comp.html", context)


def update_competition(request, id):
    b3competition = get_object_or_404(B3Competition, id=id)

    if request.method == "POST":
        form = CompForm(request.POST, instance=b3competition)
        if form.is_valid():
            form.save()
            return redirect(
                "competitions"
            )  # Redirect to the official list page or another URL
    else:
        form = CompForm(instance=b3competition)

    return render(
        request, "comps/newcomp.html", {"form": form, "b3competition": b3competition}
    )


# delete
def delete_competition(request, id):
    b3competition = get_object_or_404(B3Competition, id=id)

    if request.method == "POST":
        b3competition.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"b3competition": b3competition})


# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.db import connection



# view official details
from django.forms import inlineformset_factory



def generate_b3fixtures_view(request, b3season_id):
    b3season = get_object_or_404(B3Season, id=b3season_id)
   
    # Fetch all teams for the b3season (assuming you have a Team model)
    teams = Team.objects.filter(b3season=b3season)

    # Fetch all b3groups for the b3season
    b3groups = B3Group.objects.filter(b3season=b3season)

    # Implement your fixture generation logic here
    fixtures = []
    for b3group in b3groups:
        b3group_teams = teams.filter(b3group=b3group)
        team_count = len(b3group_teams)

        # Simple round-robin algorithm for b3group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = B3Fixture(
                    b3season=b3season,
                    b3group=b3group,
                    team1=b3group_teams[i],
                    team2=b3group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    B3Fixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_b3fixtures_view(request, id):
    fixture = get_object_or_404(B3Fixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "b3season", fixture.b3season_id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "b3fixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # Posts details......................................................
def FixtureDetail(request, id):
    fixture = get_object_or_404(B3Fixture, id=id)
    # match_official = match_official.objects.filter(fixture=fixture).order_by('-Created')
    new_official = None
   
    # new_comment_reply = None

    if request.method == 'POST':
        cform = MatchOfficialForm(request.POST, request.FILES)

        if cform.is_valid():
            new_official = cform.save(commit=False)
            new_official.fixture = fixture
            new_official.save()
            return redirect('fixture',id)
    else: 
        cform = MatchOfficialForm()
    if request.method == 'POST':
        cform = MatchOfficialForm(request.POST, request.FILES)

        if cform.is_valid():
            new_official = cform.save(commit=False)
            new_official.fixture = fixture
            new_official.save()
            return redirect('fixture',id)
    else: 
        cform = MatchOfficialForm()
        
   

    context = {'fixture': fixture,'cform':cform}

    return render(request, 'fixtures/fixture.html', context)
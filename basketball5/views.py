from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *
from .filters import *
from accounts.models import Sport
from django.http import JsonResponse

# Create your views here.


# @school_required
def create_competition(request):
    baketball5 = Sport.objects.filter(id=12).first()
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.sport = baketball5
            comp.save()

            return redirect("b5comps")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = CompForm()

    return render(request, "comps/newb5comp.html", {"form": form})


# template


# officials list, tuple or array
def competitions(request):
    competitions = B5Competition.objects.all()
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
    return render(request, "basketball5/competitions.html", context)


# view official details
def competition_details(request, id):
    b5competition = B5Competition.objects.get(id=id)
    b5seasons = B5Season.objects.filter(b5competition=b5competition)
    context = {"b5competition": b5competition, "b5seasons": b5seasons}
    return render(request, "comps/b5comp.html", context)


def update_competition(request, id):
    b5competition = get_object_or_404(B5Competition, id=id)

    if request.method == "POST":
        form = CompForm(request.POST, instance=b5competition)
        if form.is_valid():
            form.save()
            return redirect(
                "competitions"
            )  # Redirect to the official list page or another URL
    else:
        form = CompForm(instance=b5competition)

    return render(
        request, "comps/newcomp.html", {"form": form, "b5competition": b5competition}
    )


# delete
def delete_competition(request, id):
    b5competition = get_object_or_404(B5Competition, id=id)

    if request.method == "POST":
        b5competition.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"b5competition": b5competition})


# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import B5Season
from .forms import B5SeasonForm
from django.db import connection




# view official details
from django.forms import inlineformset_factory

def generate_fixtures_view(request, b5season_id):
    b5season = get_object_or_404(B5Season, id=b5season_id)
   
    # Fetch all teams for the b5season (assuming you have a Team model)
    teams = Team.objects.filter(b5season=b5season)

    # Fetch all b5groups for the b5season
    b5groups = B5Group.objects.filter(b5season=b5season)

    # Implement your fixture generation logic here
    fixtures = []
    for b5group in b5groups:
        b5group_teams = teams.filter(b5group=b5group)
        team_count = len(b5group_teams)

        # Simple round-robin algorithm for b5group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = B5Fixture(
                    b5season=b5season,
                    b5group=b5group,
                    team1=b5group_teams[i],
                    team2=b5group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    B5Fixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_b5fixtures_view(request, id):
    fixture = get_object_or_404(B5Fixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "b5season", fixture.b5season_id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "b5fixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # Posts details......................................................
def FixtureDetail(request, id):
    fixture = get_object_or_404(B5Fixture, id=id)
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
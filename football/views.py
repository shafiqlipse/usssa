from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *
from .filters import *
from accounts.models import Sport
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Season

from django.db import connection

# template


# Create your views here.
def Football(request):
    football = Sport.objects.get(id=9)
    comps = Competition.objects.filter(sport=football)

    if request.method == "POST":
        cform = CompForm(request.POST, request.FILES)

        if cform.is_valid():
            competn = cform.save(commit=False)
            competn.sport = football
            competn.save()
            return HttpResponseRedirect(reverse("football"))
    else:
        cform = CompForm()

    # If form is invalid, re-render form with errors
    context = {"cform": cform, "comps": comps}
    return render(request, "football/football.html", context)


def create_competition(request):
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("comps")  # Replace with the actual success URL name
    else:
        form = CompForm()

    return render(request, "competition/season_create.html", {"form": form})


def update_competition(request, id):
    competition = get_object_or_404(Competition, id=id)

    if request.method == "POST":
        form = CompForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            return redirect(
                "competitions"
            )  # Redirect to the official list page or another URL
    else:
        form = CompForm(instance=competition)

    return render(
        request, "comps/newcomp.html", {"form": form, "competition": competition}
    )


# delete
def delete_competition(request, id):
    competition = get_object_or_404(Competition, id=id)

    if request.method == "POST":
        competition.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"competition": competition})


# view official details
from django.forms import inlineformset_factory


def competition_details(request, id):
    competition = get_object_or_404(Competition, id=id)

    # Create a formset for editing existing groups
    GroupFormset = inlineformset_factory(
        Competition,
        Group,
        form=GroupForm,
        extra=0,  # Set extra=0 to prevent new group creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=competition)
        if formset.is_valid():
            formset.save()
            return redirect("comp", competition.id)
    else:
        formset = GroupFormset(instance=competition)

    fixtures = Fixture.objects.filter(competition=competition)
    context = {"competition": competition, "formset": formset, "fixtures": fixtures}
    return render(request, "competition/season_detail.html", context)


def generate_fixtures_view(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    season = competition.season

    # Fetch all teams for the competition (assuming you have a Team model)
    teams = Team.objects.all()

    # Fetch all groups for the competition
    groups = Group.objects.filter(competition=competition)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(group=group)
        team_count = len(group_teams)

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = Fixture(
                    competition=competition,
                    season=season,
                    group=group,
                    team1=group_teams[i],
                    team2=group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    Fixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_fixtures_view(request, id):
    fixture = get_object_or_404(Fixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "fixture", id=id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "fixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # # Posts details......................................................
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Fixture, MatchEvent
# from .forms import MatchOfficialForm, MatchEventForm


def FixtureDetail(request, id):
    fixture = get_object_or_404(Fixture, id=id)
    officials = match_official.objects.filter(fixture_id=id)
    events = MatchEvent.objects.filter(match_id=id)

    if request.method == "POST":

        cform = MatchOfficialForm(request.POST, request.FILES)
        if cform.is_valid():
            new_official = cform.save(commit=False)
            new_official.fixture = fixture
            new_official.save()
            return redirect("fixture", id=id)

    else:
        cform = MatchOfficialForm()

    context = {
        "fixture": fixture,
        "cform": cform,
        "officials": officials,
        "events": events,
    }

    return render(request, "fixtures/fixture.html", context)


def FixtureEvent(request, id):
    fixture = get_object_or_404(Fixture, id=id)

    if request.method == "POST":

        eform = MatchEventForm(request.POST)
        if eform.is_valid():
            new_event = eform.save(commit=False)
            new_event.match = fixture
            new_event.save()
            return redirect("fixture", id=id)
    else:

        eform = MatchEventForm()

    context = {
        "fixture": fixture,
        "eform": eform,
    }

    return render(request, "fixtures/event.html", context)

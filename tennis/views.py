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
    football = Sport.objects.filter(id=1).first()
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.sport = football
            comp.save()

            return redirect("comps")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = CompForm()

    return render(request, "comps/newcomp.html", {"form": form})


# template


# officials list, tuple or array
def competitions(request):
    competitions = Competition.objects.all()
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
    return render(request, "football/competitions.html", context)


# view official details
def competition_details(request, id):
    competition = Competition.objects.get(id=id)
    seasons = Season.objects.filter(competition=competition)
    context = {"competition": competition, "seasons": seasons}
    return render(request, "comps/comp.html", context)


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


# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Season
from .forms import SeasonForm
from django.db import connection


class SeasonCreateView(CreateView):
    model = Season
    form_class = SeasonForm
    template_name = "season/season_create.html"  # Create a template for this view
    success_url = reverse_lazy(
        "create_season"
    )  # Replace with the actual success URL name


# view official details
from django.forms import inlineformset_factory


def season_details(request, id):
    season = get_object_or_404(Season, id=id)

    # Create a formset for editing existing groups
    GroupFormset = inlineformset_factory(
        Season,
        Group,
        form=GroupForm,
        extra=0,  # Set extra=0 to prevent new group creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=season)
        if formset.is_valid():
            formset.save()
            return redirect("season", season.id)
    else:
        formset = GroupFormset(instance=season)

    fixtures = Fixture.objects.filter(season=season)
    context = {"season": season, "formset": formset, "fixtures": fixtures}
    return render(request, "season/season_detail.html", context)


def generate_fixtures_view(request, season_id):
    season = get_object_or_404(Season, id=season_id)

    # Fetch all teams for the season (assuming you have a Team model)
    teams = Team.objects.filter(season=season)

    # Fetch all groups for the season
    groups = Group.objects.filter(season=season)

    # Implement your fixture generation logic here
    fixtures = []
    for group in groups:
        group_teams = teams.filter(group=group)
        team_count = len(group_teams)

        # Simple round-robin algorithm for group stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = Fixture(
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
                "season", fixture.season_id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "fixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # Posts details......................................................
def FixtureDetail(request, id):
    fixture = get_object_or_404(Fixture, id=id)
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
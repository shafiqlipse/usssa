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
def Ncreate_competition(request):
    netball = Sport.objects.filter(id=2).first()
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.sport = netball
            comp.save()

            return redirect("ncomps")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = CompForm()

    return render(request, "comps/newncomp.html", {"form": form})


# template


# officials list, tuple or array
def Ncompetitions(request):
    competitions = NCompetition.objects.all()
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
    return render(request, "netball/competitions.html", context)


# view official details
def Ncompetition_details(request, id):
    competition = NCompetition.objects.get(id=id)
    seasons = NSeason.objects.filter(ncompetition=competition)
    context = {"competition": competition, "seasons": seasons}
    return render(request, "comps/ncomp.html", context)


def Nupdate_competition(request, id):
    competition = get_object_or_404(NCompetition, id=id)

    if request.method == "POST":
        form = CompForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            return redirect(
                "ncompetitions"
            )  # Redirect to the official list page or another URL
    else:
        form = CompForm(instance=competition)

    return render(
        request, "comps/newncomp.html", {"form": form, "competition": competition}
    )


# delete
def Ndelete_competition(request, id):
    competition = get_object_or_404(NCompetition, id=id)

    if request.method == "POST":
        competition.delete()
        return redirect("ncomps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_ncomp.html", {"competition": competition})


# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import NSeason
from .forms import SeasonForm
from django.db import connection


class NSeasonCreateView(CreateView):
    model = NSeason
    form_class = SeasonForm
    template_name = "nseason/season_create.html"  # Create a template for this view
    success_url = reverse_lazy(
        "create_season"
    )  # Replace with the actual success URL name


# view official details
from django.forms import inlineformset_factory


def Nseason_details(request, id):
    nseason = get_object_or_404(NSeason, id=id)

    # Create a formset for editing existing groups
    GroupFormset = inlineformset_factory(
        NSeason,
        NGroup,
        form=GroupForm,
        extra=0,  # Set extra=0 to prevent new ngroup creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=nseason)
        if formset.is_valid():
            formset.save()
            return redirect("nseason", nseason.id)
    else:
        formset = GroupFormset(instance=nseason)

    fixtures = NFixture.objects.filter(nseason=nseason)
    context = {"nseason": nseason, "formset": formset, "fixtures": fixtures}
    return render(request, "nseason/nseason_detail.html", context)


def Ngenerate_fixtures_view(request, nseason_id):
    nseason = get_object_or_404(NSeason, id=nseason_id)
    print(nseason)

    # Fetch all teams for the nseason (assuming you have a Team model)
    teams = Team.objects.filter(nseason=nseason)

    # Fetch all groups for the nseason
    ngroups = NGroup.objects.filter(nseason=nseason)

    # Implement your fixture generation logic here
    fixtures = []
    for ngroup in ngroups:
        group_teams = teams.filter(ngroup=ngroup)
        team_count = len(group_teams)

        # Simple round-robin algorithm for ngroup stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = NFixture(
                    nseason=nseason,
                    ngroup=ngroup,
                    team1=group_teams[i],
                    team2=group_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    NFixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def Nedit_fixtures_view(request, id):
    fixture = get_object_or_404(NFixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "nseason", fixture.nseason_id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "fixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # Posts details......................................................
def NFixtureDetail(request, id):
    fixture = get_object_or_404(NFixture, id=id)
    # match_official = match_official.objects.filter(fixture=fixture).order_by('-Created')
    new_official = None

    # new_comment_reply = None

    if request.method == "POST":
        cform = MatchOfficialForm(request.POST, request.FILES)

        if cform.is_valid():
            new_official = cform.save(commit=False)
            new_official.fixture = fixture
            new_official.save()
            return redirect("fixture", id)
    else:
        cform = MatchOfficialForm()
    if request.method == "POST":
        cform = MatchOfficialForm(request.POST, request.FILES)

        if cform.is_valid():
            new_official = cform.save(commit=False)
            new_official.fixture = fixture
            new_official.save()
            return redirect("fixture", id)
    else:
        cform = MatchOfficialForm()

    context = {"fixture": fixture, "cform": cform}

    return render(request, "fixtures/fixture.html", context)

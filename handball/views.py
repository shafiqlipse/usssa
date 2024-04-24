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
    baketball3 = Sport.objects.filter(id=6).first()
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.sport = baketball3
            comp.save()

            return redirect("hcomps")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = CompForm()

    return render(request, "hcomps/newcomp.html", {"form": form})


# template


# officials list, tuple or array
def competitions(request):
    competitions = HCompetition.objects.all()
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
    return render(request, "handball/competitions.html", context)


# view official details
def competition_details(request, id):
    hcompetition = HCompetition.objects.get(id=id)
    hseasons = HSeason.objects.filter(hcompetition=hcompetition)
    context = {"hcompetition": hcompetition, "hseasons": hseasons}
    return render(request, "hcomps/comp.html", context)


def update_competition(request, id):
    hcompetition = get_object_or_404(HCompetition, id=id)

    if request.method == "POST":
        form = CompForm(request.POST, instance=hcompetition)
        if form.is_valid():
            form.save()
            return redirect(
                "competitions"
            )  # Redirect to the official list page or another URL
    else:
        form = CompForm(instance=hcompetition)

    return render(
        request, "comps/newcomp.html", {"form": form, "hcompetition": hcompetition}
    )


# delete
def delete_competition(request, id):
    hcompetition = get_object_or_404(HCompetition, id=id)

    if request.method == "POST":
        hcompetition.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_comp.html", {"hcompetition": hcompetition})


# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import HSeason
from .forms import HSeasonForm
from django.db import connection


class HSeasonCreateView(CreateView):
    model = HSeason
    form_class = HSeasonForm
    template_name = "hseason/season_create.html"  # Create a template for this view
    success_url = reverse_lazy(
        "create_hseason"
    )  # Replace with the actual success URL name


# view official details
from django.forms import inlineformset_factory


def season_details(request, id):
    hseason = get_object_or_404(HSeason, id=id)

    # Create a formset for editing existing hgroups
    HGroupFormset = inlineformset_factory(
        HSeason,
        HGroup,
        form=HGroupForm,
        extra=0,  # Set extra=0 to prevent new hgroup creation
    )

    if request.method == "POST":
        formset = HGroupFormset(request.POST, instance=hseason)
        if formset.is_valid():
            formset.save()
            return redirect("hseason", hseason.id)
    else:
        formset = HGroupFormset(instance=hseason)

    fixtures = HFixture.objects.filter(hseason=hseason)
    context = {"hseason": hseason, "formset": formset, "fixtures": fixtures}
    return render(request, "hseason/season_detail.html", context)


def generate_hfixtures_view(request, hseason_id):
    hseason = get_object_or_404(HSeason, id=hseason_id)
   
    # Fetch all teams for the hseason (assuming you have a Team model)
    teams = Team.objects.filter(hseason=hseason)

    # Fetch all hgroups for the hseason
    hgroups = HGroup.objects.filter(hseason=hseason)

    # Implement your fixture generation logic here
    fixtures = []
    for hgroup in hgroups:
        hgroup_teams = teams.filter(hgroup=hgroup)
        team_count = len(hgroup_teams)

        # Simple round-robin algorithm for hgroup stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = HFixture(
                    hseason=hseason,
                    hgroup=hgroup,
                    team1=hgroup_teams[i],
                    team2=hgroup_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    HFixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_hfixtures_view(request, id):
    fixture = get_object_or_404(HFixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "hseason", fixture.hseason_id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "hfixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # Posts details......................................................
def FixtureDetail(request, id):
    fixture = get_object_or_404(HFixture, id=id)
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
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

            return redirect("vcomps")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = CompForm()

    return render(request, "comps/newvcomp.html", {"form": form})


# template


# officials list, tuple or array
def competitions(request):
    competitions = VCompetition.objects.all()
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
    return render(request, "volleyball/competitions.html", context)


# view official details
def competition_details(request, id):
    competition = VCompetition.objects.get(id=id)
    vseasons = VSeason.objects.filter(vcompetition=competition)
    context = {"competition": competition, "vseasons": vseasons}
    return render(request, "comps/vcomp.html", context)


def update_competition(request, id):
    competition = get_object_or_404(VCompetition, id=id)

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
        request, "comps/newvcomp.html", {"form": form, "competition": competition}
    )


# delete
def delete_competition(request, id):
    competition = get_object_or_404(VCompetition, id=id)

    if request.method == "POST":
        competition.delete()
        return redirect("comps")  # Redirect to the official list page or another URL

    return render(request, "comps/delete_vcomp.html", {"competition": competition})


# In your views.py file

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import VSeason
from .forms import SeasonForm
from django.db import connection


class SeasonCreateView(CreateView):
    model = VSeason
    form_class = SeasonForm
    template_name = "season/vseason_create.html"  # Create a template for this view
    success_url = reverse_lazy(
        "create_vseason"
    )  # Replace with the actual success URL name


# view official details
from django.forms import inlineformset_factory


def vseason_details(request, id):
    vseason = get_object_or_404(VSeason, id=id)

    # Create a formset for editing existing vgroups
    GroupFormset = inlineformset_factory(
        VSeason,
        VGroup,
        form=GroupForm,
        extra=0,  # Set extra=0 to prevent new vgroup creation
    )

    if request.method == "POST":
        formset = GroupFormset(request.POST, instance=vseason)
        if formset.is_valid():
            formset.save()
            return redirect("vseason", vseason.id)
    else:
        formset = GroupFormset(instance=vseason)

    fixtures = VFixture.objects.filter(vseason=vseason)
    context = {"vseason": vseason, "formset": formset, "fixtures": fixtures}
    return render(request, "season/vseason_detail.html", context)


def generate_vfixtures_view(request, vseason_id):
    vseason = get_object_or_404(VSeason, id=vseason_id)

    # Fetch all teams for the vseason (assuming you have a Team model)
    teams = Team.objects.filter(vseason=vseason)

    # Fetch all vgroups for the vseason
    vgroups = VGroup.objects.filter(vseason=vseason)

    # Implement your fixture generation logic here
    fixtures = []
    for vgroup in vgroups:
        vgroup_teams = teams.filter(vgroup=vgroup)
        team_count = len(vgroup_teams)

        # Simple round-robin algorithm for vgroup stage fixtures
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                fixture = VFixture(
                    vseason=vseason,
                    vgroup=vgroup,
                    team1=vgroup_teams[i],
                    team2=vgroup_teams[j],
                    # You may set other fixture properties such as venue, date, etc.
                )
                fixtures.append(fixture)

    # Bulk create fixtures
    VFixture.objects.bulk_create(fixtures)

    return JsonResponse({"success": True, "message": "Fixtures generated successfully"})


def edit_fixtures_view(request, id):
    fixture = get_object_or_404(VFixture, id=id)

    if request.method == "POST":
        form = FixtureForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect(
                "vseason", fixture.vseason_id
            )  # Replace 'success_url' with the actual URL
    else:
        form = FixtureForm(instance=fixture)

    return render(
        request, "vfixtures/edit_fixture.html", {"form": form, "fixture": fixture}
    )


# # Posts details......................................................
def FixtureDetail(request, id):
    fixture = get_object_or_404(VFixture, id=id)
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
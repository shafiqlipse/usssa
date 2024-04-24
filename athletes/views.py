from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.decorators import school_required, anonymous_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .filters import AthleteFilter, TeamFilter
from .forms import *
from school.models import school_official
from django.http import JsonResponse
import datetime
from django.contrib import messages


# # Create your views here.


def get_athletes(request):
    # Get the school associated with the logged-in user
    school_id = request.user.school_profile

    sport_id = request.GET.get("sport_id")
    gender = request.GET.get("gender")
    age_id = request.GET.get("age_id")

    # Start with the base queryset for athletes in the user's school
    athletes = Athlete.objects.filter(school=school_id, sport=sport_id)

    # Apply additional filters for sport, gender, and age if provided

    if gender:
        athletes = athletes.filter(gender=gender)

    if age_id:
        athletes = athletes.filter(age_id=age_id)

    # Retrieve only the necessary fields
    athletes = athletes.values("id", "name")

    # Wrap the athletes array in a JSON object with a 'athletes' property
    data = {"athletes": list(athletes)}

    return JsonResponse(data)


def get_officials(request):
    # Get the official associated with the logged-in user
    school = request.user.school_profile

    # Filter officials based on the logged-in user
    officials = school_official.objects.filter(school=school)

    # Retrieve only the necessary fields
    officials = officials.values("id", "name")

    # Wrap the officials array in a JSON object with an 'officials' property
    data = {"officials": list(officials)}

    return JsonResponse(data)


@school_required
def newAthlete(request):
    school = request.user.school_profile
    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_athlete = form.save(commit=False)
                new_athlete.school = school
                new_athlete.save()
                messages.success(request, "Athlete added successfully!")
                return redirect("athletes")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = NewAthleteForm()

    return render(request, "athletes/newathlete.html", {"form": form, "school": school})


# # Athletes details......................................................
def AthleteDetail(request, id):
    athlete = get_object_or_404(Athlete, id=id)
    relatedathletes = Athlete.objects.filter(sport=athlete.sport).exclude(id=id)
    # breadcrumbs = [{'url': '/', 'name': 'Home'},
    #                {'url': f'/team/{athlete.team.id}/', 'name': 'Category'},
    #             #    {'url': f'/product/{product_id}/', 'name': 'Product'}
    #             ]
    context = {
        "athlete": athlete,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "athletes/athlete.html", context)


# # # Athletes details......................................................


# def school_import_view(request):
#     iform = AthleteImportForm()  # Move this line outside the conditional block

#     if request.method == "POST":
#         form_class = AthleteImportForm
#         iform = form_class(request.POST, request.FILES)

#         if iform.is_valid():
#             # Create a resource dynamically for the Athlete model
#             AthleteResource = modelresource_factory(model=Athlete)()

#             # Import the data using the resource
#             # Pass a new HttpRequest object to import_data
#             fake_request = HttpRequest()
#             fake_request.method = "POST"

#             result = AthleteResource.import_data(
#                 request.FILES["csv_file"],
#                 dry_run=False,
#                 raise_errors=True,
#                 request=fake_request,
#             )

#             if result.has_errors():
#                 # Handle errors appropriately
#                 messages.error(request, "There were errors during the import.")
#             else:
#                 # Save the imported data
#                 result.save()
#                 messages.success(request, "Athletes imported successfully.")

#             return redirect("schooldash")  # Redirect to your school dashboard URL

#     return render(request, "Dashboard/importathletes.html", {"iform": iform})


# @login_required(login_url="login")
def athletes(request):
    athletes = Athlete.objects.filter(school=request.user.school_profile)

    context = {
        "athletes": athletes,
    }

    return render(request, "athletes/athletes.html", context)


# @login_required(login_url="login")
def registration(request):
    athletes = Athlete.objects.filter(school=request.user.school_profile)

    context = {
        "athletes": athletes,
    }

    return render(request, "athletes/reg.html", context)


# @login_required(login_url="login")
def teamlist(request):
    user = request.user
    school = user.school_profile
    teams = Team.objects.filter(school=school)
    myteams = Team.objects.filter(school_id=user.id)
    myFilter = TeamFilter(request.GET, queryset=myteams)
    # myFilter = AthleteFilter(request.GET, queryset=athletes)
    teamlist = myFilter.qs
    context = {"teams": teams, "teamlist": teamlist, "myFilter": myFilter}

    return render(request, "teams/teams.html", context)


# # # news Athlete creation.....................................................
# # @login_required(login_url="login")
# from django.shortcuts import get_object_or_404

# from django.http import JsonResponse
# from .models import Age
# import datetime


def calculate_age_choices(request):
    date_of_birth_str = request.GET.get("date_of_birth")

    # Check if date_of_birth_str is None
    if date_of_birth_str is None:
        return JsonResponse({"error": "Date of birth is missing"}, status=400)

    # Convert date_of_birth string to a datetime.date object
    date_of_birth = datetime.datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()

    # Calculate the athlete's age based on the date of birth
    current_year = datetime.date.today().year
    calculated_age = (
        current_year
        - date_of_birth.year
        - (
            (datetime.date.today().month, datetime.date.today().day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )

    # Filter the Age model to get age choices based on the calculated age
    age_choices = Age.objects.filter(
        min_age__lte=calculated_age, max_age__gte=calculated_age
    ).values_list("id", "name")

    # Prepare the JSON response
    response_data = {"ages": list(age_choices)}

    return JsonResponse(response_data)


# from django.contrib import messages
from django.views.generic import UpdateView

# # # Athlete update page-----------------------------------------------------------------------
# # @login_required(login_url="login")
# @school_required
class AthleteUpdate(UpdateView):
    model = Athlete
    form_class = UpdateAthleteForm
    template_name = 'athletes/updateatlete.html'
    pk_url_kwarg = 'id'
    success_url = '/athletes/'  # Specify the URL to redirect to after successful update

    def form_valid(self, form):
        # Update only the desired fields
        self.object.name = form.cleaned_data.get('name', self.object.name)
        self.object.gender = form.cleaned_data.get('lname', self.object.gender)
        self.object.photo = form.cleaned_data.get('photo', self.object.photo)
        self.object.save()
        success_url = reverse_lazy('athletes')


@school_required
def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.school = request.user.school_profile
            team.save()
            athletes = form.cleaned_data.get(
                "athletes"
            )  # Replace 'athletes' with the actual form field name
            team.athletes.set(athletes)
            team.save()

            return redirect("teams")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = TeamForm()
        error_message = None

    return render(
        request, "teams/newteam.html", {"form": form, "error_message": error_message}
    )


#     # template

#     # update school team


# @school_required
def update_team(request, id):
    team = get_object_or_404(Team, pk=id)

    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect("teams")  # Redirect to the team list page or another URL
    else:
        form = TeamForm(instance=team)

    return render(request, "teams/newteam.html", {"form": form, "team": team})


# # view team details
# from football.models import Fixture


# def team_details(request, id):
#     team = Team.objects.get(pk=id)
#     fixtures = Fixture.objects.filter(competition__teams=team)
#     athletes = team.athletes.all()
#     context = {"team": team, "fixtures": fixtures, "athletes": athletes}
#     return render(request, "teams/team.html", context)


# # delete team
@school_required
def delete_team(request, id):
    team = get_object_or_404(Team, pk=id)

    if request.method == "POST":
        team.delete()
        return redirect("teams")  # Redirect to the team list page or another URL

    return render(request, "teams/delete_team.html", {"team": team})

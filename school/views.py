from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Region, Zone, Sport
from .models import School, school_official
from accounts.decorators import school_required
from django.contrib.auth.decorators import login_required
from .forms import SchoolProfileForm, OfficialForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import OfficialFilter


# Create your views here.
# @school_required
def School(request):
    regions = Region.objects.all()
    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES)
        if form.is_valid():
            schoolX = form.save(commit=False)
            schoolX.status ="Inactive"
            schoolX.save()
            messages.success(request, "Account completed successfully!")
            return redirect("confirm")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = SchoolProfileForm()
    context = {"form": form, "regions": regions}
    return render(request, "profile/create_school.html", context)


def confirm(request):
    context = {}
    return render(request, "dashboard/school_dash.html", context)


# school update view
@login_required
def school_update(request):
    # Get the SchoolProfile instance associated with the logged-in user
    school_profile = request.user.school_profile
    regions = Region.objects.all()
    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES, instance=school_profile)
        if form.is_valid():
            profile = form.save(commit=False)

            # Check if an image was provided in the form
            if "badge" in request.FILES:
                profile.profile_image = request.FILES[
                    "badge"
                ]  # Assign the image to the profile

            form.save()
            # Redirect to the profile view after saving changes
            return redirect("schoolprofile", request.user.id)

    else:
        form = SchoolProfileForm(instance=school_profile)

    context = {"form": form, "regions": regions}

    return render(request, "profile/create_school.html", context)


# Create your headteacher views here.


# Create your headteacher views here.
@school_required
def School_official(request):
    if request.method == "POST":
        form = OfficialForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                schoolX = form.save(commit=False)
                schoolX.school = request.user.school_profile
                schoolX.save()
                messages.success(request, "Account completed successfully!")
                return redirect("sofficials")

            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = OfficialForm()
    context = {"form": form}
    return render(request, "officials/new_official.html", context)


# many officials
def School_officials(request):
    officials = school_official.objects.filter(school=request.user.school_profile)

    # officialFilter = OfficialFilter(request.GET, queryset=officials)

    context = {
        "officials": officials,
    }

    return render(request, "officials/school_officials.html", context)


@school_required
def edit_official(request, pk):
    official = get_object_or_404(school_official, pk=pk)

    if request.method == "POST":
        form = OfficialForm(request.POST, request.FILES, instance=official)
        if form.is_valid():
            official = form.save(commit=False)
            # You might want to set the user associated with the official here
            # For example, official.user = request.user
            official.save()
            return redirect("officials")  # Redirect to the list view
    else:
        form = OfficialForm(instance=official)

    return render(
        request, "officials/new_official.html", {"form": form, "official": official}
    )


@school_required
def school_dashboard(request):
    # athletes_count = Athlete.objects.filter(school=request.user).count()
    # athletes = Athlete.objects.filter(school=request.user)
    # team_boys = Team.objects.filter(school=request.user, gender="male").count()
    Official_boys = school_official.objects.filter(
        user=request.user, gender="M"
    ).count()
    # boys = Athlete.objects.filter(school=request.user, gender="male").count()
    # team_girls = Team.objects.filter(school=request.user, gender="female").count()
    Official_girls = school_official.objects.filter(
        user=request.user, gender="F"
    ).count()
    # girls = Athlete.objects.filter(school=request.user, gender="female").count()
    officials_count = school_official.objects.filter(user=request.user).count()
    # teams_count = Team.objects.filter(school=request.user).count()
    # unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    # headteacher = HeadTeacher.objects.filter(user=request.user)
    context = {
        # "athletes_count": athletes_count,
        "officials_count": officials_count,
        # "teams_count": teams_count,
        # "unread_count": unread_count,
        # "boys": boys,
        # "team_boys": team_boys,
        "Official_boys": Official_boys,
        # "team_girls": team_girls,
        "Official_girls": Official_girls,
        # "girls": girls,
        # "athletes": athletes,
        # "headteacher": headteacher,
    }
    return render(request, "dashboard/school_dash.html", context)


# def school_profile(request, id):
#     officials = school_official.objects.filter(user_id=id)
#     myFilter = OfficialFilter(request.GET, queryset=officials)
#     officiallist = myFilter.qs
#     # athletes
#     athletes = Athlete.objects.filter(school_id=id)
#     athletesFilter = AthleteFilter(request.GET, queryset=athletes)
#     athleteslist = athletesFilter.qs
#     # teams
#     teams = Team.objects.filter(school_id=id)
#     profile = School.object.get(user_id=id)

#     teamsFilter = TeamFilter(request.GET, queryset=teams)
#     teamlist = teamsFilter.qs

#     context = {
#         "profile": profile,
#         "officiallist": officiallist,
#         "teamsFilter": teamsFilter,
#         "myFilter": myFilter,
#         "teamlist": teamlist,
#         "athleteslist": athleteslist,
#         "athletesFilter": athletesFilter,
#     }
#     return render(request, "profile/school_profile.html", context)

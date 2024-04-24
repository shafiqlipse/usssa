from django.shortcuts import render, redirect
from accounts.decorators import school_required, anonymous_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .forms import SchoolRegistrationForm
from school.models import School
from .models import User, Zone, Region,District
from django.contrib import messages


# Create your views here.
def get_districts(request):
    region_id = request.GET.get("region_id")
    districts = District.objects.filter(region_id=region_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)

# Create your views here.
def get_zones(request):
    region_id = request.GET.get("region_id")
    zones = Zone.objects.filter(region_id=region_id).values("id", "name")
    return JsonResponse(list(zones), safe=False)


# dashboards views
def dashboard(request):
    context = {}
    return render(request, "dashboard/dashboard.html", context)


#  auth views
@anonymous_required
def school_registration(request):
    if request.method == "POST":
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Create the user object without saving to the database
            user.is_school = True  # Set is_school to True
            user.save()  # Save the user object with is_school set to True

            # Log in the user
            login(request, user)

            return redirect("school")
    else:
        form = SchoolRegistrationForm()
    return render(request, "account/sregister.html", {"form": form})


@anonymous_required
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user without logging in
            user = form.get_user()
            login(request, user)

            # Check if the user is a school
            if user.is_school:
                # Check if the school user has a profile
                profile = School.objects.filter(user=user).first()
                if profile:
                    messages.info(request, "Welcome back!")
                    return redirect(
                        "dashboard"
                    )  # Redirect to home for school users with a profile
                else:
                    messages.info(
                        request, "Welcome! Please complete your school profile."
                    )
                    return redirect(
                        "school"
                    )  # Adjust the URL name for your create school profile view

                # If the user is not a school, log in and redirect to dashboard
            messages.success(request, "Login successful.")
            return redirect("dashboard")  # Adjust the URL name for your dashboard view
        else:
            messages.error(request, "Error in login. Please check your credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    # if user.is_authenticated:
    logout(request)
    return redirect("login")


def custom_404(request, exception):
    return render(request, "account/custom404.html", {}, status=404)

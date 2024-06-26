from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import *

from .models import *

from accounts.forms import *
from school.forms import *
from django.utils import timezone


from django.contrib import messages
from django.http import JsonResponse
from accounts.decorators import (
    school_required,
    staff_required,
    login_required,
)
import traceback


# Create your views here.
@login_required
def dashboard(request):
    schools = School.objects.all()
    schools_count = School.objects.all().count
    # schools_today = School.objects.filter(created_at__date=today).count
    athletes = Athlete.objects.all()
    athletes_count = Athlete.objects.all().count
    officials_count = school_official.objects.all().count
    athletes_bcount = Athlete.objects.filter(gender="male").count
    athletes_gcount = Athlete.objects.filter(gender="female").count
    officials_bcount = school_official.objects.filter(gender="M").count
    officials_gcount = school_official.objects.filter(gender="F").count
    context = {
        "athletes": athletes,
        "schools": schools,
        "athletes_count": athletes_count,
        # "schools_today": schools_today,
        "schools_count": schools_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
    }
    return render(request, "dashboard/dashboard.html", context)


# https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment


# Create your views here.


# schools list, tuple or array
@staff_required
def schools(request):

    schools = School.objects.all()

    context = {
        "schools": schools,
        # "teamsFilter": teams
    }
    return render(request, "dashboard/schools.html", context)


# schools list, tuple or array
@staff_required
def all_athletes(request):

    athletes = Athlete.objects.all()

    context = {
        "athletes": athletes,
    }
    return render(request, "dashboard/athletes.html", context)


# schools list, tuple or array
@staff_required
def all_officials(request):

    officilas = school_official.objects.all()

    context = {
        "officilas": officilas,
    }
    return render(request, "dashboard/officials.html", context)


# @staff_required
@login_required
def school_detail(request, id):
    school = School.objects.get(id=id)
    officials = school_official.objects.filter(school_id=id)
    off = school_official.objects.filter(school_id=id).count
    athletes = Athlete.objects.filter(school_id=id)
    ath = Athlete.objects.filter(school_id=id).count

    # new_comment_reply = None

    context = {
        "schools": schools,
        "school": school,
        "athletes": athletes,
        "ath": ath,
        "off": off,
        "officials": officials,
    }
    return render(request, "school/school.html", context)


# schools list, tuple or array
@login_required
def Tournaments(request):

    # schools = school.objects.all()

    # # schoolFilter = schoolFilter(request.GET, queryset=schools)
    # myFilter = schoolFilter(request.GET, queryset=schools)

    # schoollist = myFilter.qs

    # items_per_page = 10

    # paginator = Paginator(schoollist, items_per_page)
    # page = request.GET.get("page")

    # try:
    #     schoollist = paginator.page(page)
    # except PageNotAnInteger:
    #     # If the page is not an integer, deliver the first page
    #     schoollist = paginator.page(1)
    # except EmptyPage:
    #     # If the page is out of range, deliver the last page
    #     schoollist = paginator.page(paginator.num_pages)
    context = {
        #     "schoollist": schoollist,
        #     # "teamsFilter": teamsFilter,
        #     "myFilter": myFilter,
        #     # "teamlist": teamlist,
    }
    return render(request, "dashboard/tournaments.html", context)


# schools list, tuple or array
@login_required
def districts(request):

    districts = District.objects.all()

    # schoolFilter = schoolFilter(request.GET, queryset=schools)

    context = {
        "districts": districts,
    }
    return render(request, "dashboard/districts.html", context)


# schools list, tuple or array


@school_required
def Dash(request):
    user = request.user
    school = School.objects.get(user_id=user.id)
    officials_count = school_official.objects.filter(school_id=school.id).count()
    athletes_count = Athlete.objects.filter(school_id=school.id).count()
    officials_bcount = school_official.objects.filter(
        school_id=school.id, gender="M"
    ).count()
    officials_gcount = school_official.objects.filter(
        school_id=school.id, gender="F"
    ).count()
    athletes_gcount = Athlete.objects.filter(
        school_id=school.id, gender="Female"
    ).count()
    athletes_bcount = Athlete.objects.filter(school_id=school.id, gender="Male").count()
    officials = school_official.objects.filter(school_id=school.id)
    context = {
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
        "athletes_count": athletes_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials": officials,
        "school": school,
    }
    return render(request, "school/schoolprofile.html", context)


@login_required
def newAthlete(request):
    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_athlete = form.save(commit=False)
                new_athlete.school = request.user.school_profile.first()
                new_athlete.save()
                messages.success(request, "Athlete added successfully!")
                return redirect("athletes")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = NewAthleteForm()

    return render(request, "school/newAthlete.html", {"form": form})


# a confirmation of credentials
# @login_required
def confirmation(request):
    user = request.user
    context = {"user": user}
    return render(request, "confirm.html", context)


from django.http import JsonResponse
import datetime
from django.contrib import messages
from athletes.models import *
from athletes.forms import *


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


# # Athletes details......................................................
def AthleteDetail(request, id):
    athlete = get_object_or_404(Athlete, id=id)
    relatedathletes = Athlete.objects.filter(school=athlete.school).exclude(id=id)

    context = {
        "athlete": athlete,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "school/athlete.html", context)


@staff_required
def AthleteUpdate(request, id):
    band = Athlete.objects.get(id=id)

    if request.method == "POST":
        form = NewAthleteForm(request.POST, instance=band)
        if form.is_valid():
            form.save()

            return redirect("athletes")
    else:
        form = NewAthleteForm(instance=band)
    context = {"form": form}
    return render(request, "school/newAthlete.html", context)


# # Athletes details......................................................
def OfficialDetail(request, id):
    official = get_object_or_404(school_official, id=id)
    relatedathletes = school_official.objects.filter(school=official.school).exclude(
        id=id
    )

    context = {
        "official": official,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "school/official.html", context)


# def athlete_list(request):
#     athletes = Athlete.objects.all()
#     form = AthleteSelectionForm()

#     if request.method == "POST":
#         form = AthleteSelectionForm(request.POST)
#         if form.is_valid():
#             selected_athletes = form.cleaned_data["athletes"]
#             total_amount = 1500 * len(selected_athletes)

#             # Update the payment total_amount
#             payment, created = Payment.objects.get_or_create(is_paid=False)
#             payment.total_amount += total_amount
#             payment.save()

#             # Add selected athletes to the payment without deleting them
#             payment.athletes.add(*selected_athletes)

#             # Mark selected athletes as paid
#             Athlete.objects.filter(
#                 pk__in=[athlete.pk for athlete in selected_athletes]
#             ).update(is_paid=True)

#             return redirect("payment_page")

#     context = {"athletes": athletes, "form": form}
#     return render(request, "school/athlete_list.html", context)


# def payment_page(request):
#     payment = Payment.objects.filter(is_paid=False).first()
#     context = {"payment": payment}
#     return render(request, "school/payment_page.html", context)


# def process_payment(request):
#     # Retrieve the payment record for processing
#     payment = Payment.objects.filter(is_paid=False).first()

#     if payment:
#         # Process payment logic here (e.g., connect to payment gateway API, mark payment as paid)
#         # ...

#         # After successful payment processing, mark the payment as paid
#         payment.is_paid = True
#         payment.save()

#     return redirect("payment_page")

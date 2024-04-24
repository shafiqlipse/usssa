from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *
from .filters import *

# Create your views here.


# @school_required
def create_official(request):
    if request.method == "POST":
        form = OfficerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect("officials")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = OfficerForm()

    return render(request, "officials/newofficial.html", {"form": form})

    # template

    # update school official


# officials list, tuple or array
def officials(request):
    officials = Official.objects.all()

    # officialFilter = OfficialFilter(request.GET, queryset=officials)
    
    context = {
        "officials": officials,
    }
    return render(request, "officials/officials.html", context)


def update_official(request, id):
    official = get_object_or_404(Official, pk=id)

    if request.method == "POST":
        form = OfficerForm(request.POST, instance=official)
        if form.is_valid():
            form.save()
            return redirect(
                "officials"
            )  # Redirect to the official list page or another URL
    else:
        form = OfficerForm(instance=official)

    return render(
        request, "officials/update_official.html", {"form": form, "official": official}
    )


# view official details
def official_details(request, id):
    official = Official.objects.get(pk=id)

    return render(request, "officials/official.html", {"official": official})


# delete
def delete_official(request, id):
    official = get_object_or_404(Official, pk=id)

    if request.method == "POST":
        official.delete()
        return redirect(
            "officials"
        )  # Redirect to the official list page or another URL

    return render(request, "officials/delete_official.html", {"official": official})

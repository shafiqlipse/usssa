from django.shortcuts import render, get_object_or_404, redirect
from .models import TransferRequest
from athletes.models import Athlete


def athlete_list(request):
    athletes = Athlete.objects.exclude(school=request.user.school_profile)
    return render(request, "requests.html", {"athletes": athletes})


from utils.utils import (
    create_transfer_accepted_notification,
    create_transfer_rejected_notification,
)
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


# Get an instance of a logger
def transfer_athlete(request, id):
    athlete = get_object_or_404(Athlete, id=id)

    if request.method == "POST":
        try:
            # Create a TransferRequest instance and save it
            transfer_request = TransferRequest.objects.create(
                sto=athlete.school,
                sfrom=request.user.school_profile,  # Assuming request.user represents the school
                athlete=athlete,
            )

            # Add a success message
            messages.success(
                request, "Transfer request has been submitted successfully."
            )
            return redirect("tathlete_list")

        except IntegrityError as e:
            # Handle integrity errors (e.g., unique constraint violation)
            messages.error(
                request, "An error occurred while creating the transfer request."
            )
            logger.error(f"IntegrityError occurred while creating TransferRequest: {e}")
        except Exception as e:
            # Log other types of exceptions
            messages.error(request, "An error occurred. Please try again later.")
            logger.error(f"Error occurred while creating TransferRequest: {e}")

    return render(request, "requests.html", {"athlete": athlete})


def accept_transfer(request, transfer_request_id):
    transfer_request = get_object_or_404(TransferRequest, id=transfer_request_id)

    # Check if the transfer is pending
    if transfer_request.status == "Pending":
        athlete = transfer_request.athlete

        # Update the owner school of the athlete
        athlete.school = transfer_request.to_school
        athlete.save()

        # Update the transfer request status and decision date
        transfer_request.status = "Accepted"
        transfer_request.decision_date = timezone.now()
        transfer_request.save()

        # Create a notification for the parties involved
        create_transfer_accepted_notification(transfer_request)

    return redirect("transfer_request_list")


from utils.utils import create_transfer_rejected_notification


def reject_transfer(request, transfer_request_id):
    transfer_request = get_object_or_404(TransferRequest, id=transfer_request_id)

    # Check if the transfer is pending
    if transfer_request.status == "Pending":
        # Update the transfer request status and decision date
        transfer_request.status = "Rejected"
        transfer_request.decision_date = timezone.now()
        transfer_request.save()

        # Create a notification for the parties involved
        create_transfer_rejected_notification(transfer_request)

    return redirect("transfer_request_list")

# utils.py
from transfers.models import Notification


def create_transfer_accepted_notification(transfer_request):
    # Your logic for creating an accepted transfer notification
    Notification.objects.create(
        user=transfer_request.athlete.school,
        transfer_request=transfer_request,
        is_read=False,
    )


def create_transfer_rejected_notification(transfer_request):
    # Your logic for creating a rejected transfer notification
    Notification.objects.create(
        user=transfer_request.athlete.school,
        transfer_request=transfer_request,
        is_read=False,
    )

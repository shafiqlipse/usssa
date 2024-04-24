from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TransferRequest, Notification

@receiver(post_save, sender=TransferRequest)
def create_transfer_request_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the user associated with the transfer request
        Notification.objects.create(user=instance.sfrom.user, transfer_request=instance)

# In signals.py file

from django.db.models.signals import post_save
from django.dispatch import receiver
from athletes.models import (
    Team,
)  # Adjust the import based on your actual model location
from .models import VSeason, VGroup


@receiver(post_save, sender=VSeason)
def create_vgroups_for_vseason(sender, instance, created, **kwargs):
    if created:
        # Define the number of vgroups based on the 'vgroups' field in the Season model
        num_vgroups = instance.groups

        for i in range(1, num_vgroups + 1):
            vgroup_name = f"GROUP {chr(ord('A') + i - 1)}"
            VGroup.objects.create(name=vgroup_name, vseason=instance)

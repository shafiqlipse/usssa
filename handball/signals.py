# In signals.py file

from django.db.models.signals import post_save
from django.dispatch import receiver
from athletes.models import (
    Team,
)  # Adjust the import based on your actual model location
from .models import HSeason, HGroup


@receiver(post_save, sender=HSeason)
def create_groups_for_season(sender, instance, created, **kwargs):
    if created:
        # Define the number of groups based on the 'groups' field in the Season model
        num_groups = instance.groups

        for i in range(1, num_groups + 1):
            group_name = f"GROUP {chr(ord('A') + i - 1)}"
            HGroup.objects.create(name=group_name, hseason=instance)

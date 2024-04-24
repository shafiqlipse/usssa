# models.py
from django.db import models
from accounts.models import Sport


class Official(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, default="")
    phone_number = models.CharField(max_length=15)
    nin = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=10,
        choices=[
            ("Referee", "Referee"),
            ("Umpire", "Umpire"),
        ],
        null=True,
        blank=True,
    )
    sport = models.ForeignKey(Sport, related_name="official", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="photos/",
        default="/images/profile.png",
    )

    def __str__(self):
        return self.fname

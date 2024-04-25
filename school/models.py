from django.db import models
from accounts.models import User, Region, Zone, District

# Create your models here.


class School(models.Model):
    user = models.OneToOneField(
        User,
        related_name="school",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    school_name = models.CharField(max_length=100, default="")
    
    def __str__(self):
        return self.school_name


class school_official(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, default="")
    phone_number = models.CharField(max_length=15)
    nin = models.CharField(max_length=20, null=True, blank=True, default="")
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
    )
    role = models.CharField(
        max_length=55,
        choices=[
            ("Coach", "Coach"),
            ("Teacher", "Teacher"),
            ("Games Teacher", "Games Teacher"),
            ("Assistant Games Teacher", "Assistant Games Teacher"),
            ("Assistant Head Teacher", "Assistant Head Teacher"),
            ("Nurse", "Nurse"),
            ("Doctor", "Doctor"),
            ("District Education Officer", "District Education Officer"),
            ("District Sports Officer", "District Sports Officer"),
        ],
    )
    photo = models.ImageField(
        upload_to="badge/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

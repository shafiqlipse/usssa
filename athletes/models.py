from django.db import models
from accounts.models import Sport, User
from school.models import school_official, School
from datetime import datetime
from school.models import school_official
from django.db import models
from datetime import date


# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=255)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class AthleteManager(models.Manager):
    def get_queryset(self):
        today = date.today()
        queryset = super().get_queryset()
        queryset = queryset.filter(date_of_birth__lte=today)
        return queryset.annotate(
            calculated_age=models.ExpressionWrapper(
                today.year - models.F("date_of_birth__year"),
                output_field=models.IntegerField(),
            )
        )

    def filter_by_age_range(self, min_age, max_age):
        return self.get_queryset().filter(
            calculated_age__gte=min_age, calculated_age__lte=max_age
        )


class Athlete(models.Model):
    name = models.CharField(max_length=255)
    lin =  models.CharField(max_length=10,unique=True)
    sport = models.ForeignKey(Sport, related_name="sport", on_delete=models.CASCADE)
    school = models.ForeignKey(
        School, related_name="schooler", on_delete=models.CASCADE
    )
    date_of_birth = models.DateField()
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")], max_length=10
    )
    classroom = models.ForeignKey(
        Classroom, related_name="classroom", on_delete=models.CASCADE
    )
    age = models.ForeignKey(Age, related_name="age", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="athlete_photos/", blank=True, null=True)

    Parent_fname = models.CharField(max_length=100)
    Parent_lname = models.CharField(max_length=100)
    parent_email = models.EmailField(null=True, blank=True, default="")
    parent_phone_number = models.CharField(max_length=15)
    parent_nin = models.CharField(max_length=20, null=True, blank=True, default="")
    address = models.CharField(max_length=20)
    relationship = models.CharField(max_length=20)
    parent_gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        null=True,
        blank=True,
    )
    objects = AthleteManager()

    def save(self, *args, **kwargs):
        # Find the corresponding age range and assign it to the athlete
        age = date.today().year - self.date_of_birth.year
        age_range = Age.objects.filter(min_age__lte=age, max_age__gte=age).first()
        self.age = age_range

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Team(models.Model):
    sport = models.ForeignKey(Sport, related_name="sports", on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name="schools", on_delete=models.CASCADE)
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")], max_length=10
    )
    age = models.ForeignKey(Age, related_name="ages", on_delete=models.CASCADE)
    athletes = models.ManyToManyField(Athlete)
    official = models.ForeignKey(
        school_official,
        related_name="official",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.school.school_name

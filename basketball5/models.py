# models.py
from django.db import models
from athletes.models import Age, Athlete, Team
from accounts.models import Sport

# import uuid

from officials.models import Official
from accounts.models import Championship


# Create your models here.
class B5Competition(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    age = models.ForeignKey(Age, on_delete=models.CASCADE)

    comcat = models.CharField(
        choices=[("Sport", "sport"), ("Game", "game"), ("Other", "other")],
        max_length=10,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")],
        max_length=10,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class B5Season(models.Model):
    b5competition = models.ForeignKey(B5Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    participants = models.IntegerField()
    groups = models.IntegerField()
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    b5teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class B5Group(models.Model):
    b5season = models.ForeignKey(B5Season, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    b5teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class B5Fixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("RegularSeason", "Regular Season"), ("Playoffs", "Playoffs"))
    b5season = models.ForeignKey(
        B5Season, on_delete=models.CASCADE, null=True, blank=True
    )
    b5competition = models.ForeignKey(
        B5Competition, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    b5group = models.ForeignKey(B5Group, on_delete=models.CASCADE, null=True, blank=True)

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    team1 = models.ForeignKey(Team, related_name="b5team1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="b5team2", on_delete=models.CASCADE)
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    # Additional fields for 5x5 basketball
    team1_three_point_score = models.IntegerField(null=True, blank=True)
    team2_three_point_score = models.IntegerField(null=True, blank=True)
    team1_free_throw_score = models.IntegerField(null=True, blank=True)
    team2_free_throw_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id}: {self.team1} vs {self.team2}"


class match_official(models.Model):
    role = (
        ("Referee", "Referee"),
        ("Umpire", "Umpire"),
        ("First assistant", "First assistant "),
        ("Second assistant", "Second assistant "),
        ("4th Official", "4th Official"),
    )

    b5fixture = models.ForeignKey(
        B5Fixture, on_delete=models.CASCADE, null=True, blank=True
    )
    b5official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="b5official",
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture


class B5MatchEvent(models.Model):
    b5match = models.ForeignKey(B5Fixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("TwoPointScore", "Two-Point Score"),  # Represents a successful two-point shot
        (
            "ThreePointScore",
            "Three-Point Score",
        ),  # Represents a successful three-point shot
        ("FreeThrow", "Free Throw"),  # Represents a successful free throw
        ("Steal", "Steal"),
        ("Assist", "Assist"),
        ("Rebound", "Rebound"),
        ("Foul", "Foul"),
        ("Block", "Block"),
        ("Turnover", "Turnover"),
        ("Substitution", "Substitution"),
        ("Timeout", "Timeout"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )  # Example: "TwoPointScore", "ThreePointScore", "FreeThrow", "Steal"
    team = models.ForeignKey(Team, related_name="b5team", on_delete=models.CASCADE)
    athlete = models.ForeignKey(
        Athlete,
        related_name="b5athlete",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    minute = models.IntegerField()
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.event_type} at {self.minute}'"

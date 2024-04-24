# models.py
from django.db import models
from athletes.models import Age, Athlete, Team
from accounts.models import Sport
from football.models import Season

from officials.models import Official
from accounts.models import Championship


# Create your models here.
class B3Competition(models.Model):
    name = models.CharField(max_length=255)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
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





class B3Group(models.Model):
    competition = models.ForeignKey(B3Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    b3teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class B3Fixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, null=True, blank=True, related_name="b3season"
    )
    b3competition = models.ForeignKey(
        B3Competition, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    b3group = models.ForeignKey(
        B3Group, on_delete=models.CASCADE, null=True, blank=True
    )

    # Use UUIDField for match_number

    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    team1 = models.ForeignKey(Team, related_name="b3team1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="b3team2", on_delete=models.CASCADE)
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    # Additional fields for 3x3 basketball
    team1_two_point_score = models.IntegerField(null=True, blank=True)
    team2_two_point_score = models.IntegerField(null=True, blank=True)

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

    b3fixture = models.ForeignKey(
        B3Fixture, on_delete=models.CASCADE, null=True, blank=True
    )
    b3official = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="b3official",
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture


class B3MatchEvent(models.Model):
    b3match = models.ForeignKey(B3Fixture, on_delete=models.CASCADE)
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
    team = models.ForeignKey(Team, related_name="b3team", on_delete=models.CASCADE)
    athlete = models.ForeignKey(
        Athlete,
        related_name="b3athlete",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    minute = models.IntegerField()
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.event_type} at {self.minute}'"

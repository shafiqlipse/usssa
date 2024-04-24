# models.py
from django.db import models
from athletes.models import Age, Athlete, Team
from accounts.models import Sport

# import uuid
from venues.models import Venue
from officials.models import Official
from accounts.models import Championship


# Create your models here.
class NCompetition(models.Model):
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


class NSeason(models.Model):
    ncompetition = models.ForeignKey(NCompetition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    participants = models.IntegerField()
    groups = models.IntegerField()
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    nteams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class NGroup(models.Model):
    nseason = models.ForeignKey(NSeason, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    nteams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class NFixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    nseason = models.ForeignKey(
        NSeason, on_delete=models.CASCADE, null=True, blank=True
    )
    ncompetition = models.ForeignKey(
        NCompetition, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    ngroup = models.ForeignKey(NGroup, on_delete=models.CASCADE, null=True, blank=True)

    # Use UUIDField for match_number

    venue = models.ForeignKey(
        Venue, related_name="nvenue", on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateTimeField(null=True, blank=True)
    team1 = models.ForeignKey(Team, related_name="nteam1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="nteam2", on_delete=models.CASCADE)
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id}: {self.team1} vs {self.team2}"


class Nmatch_official(models.Model):
    role = (
        ("Referee", "Referee"),
        ("Umpire", "Umpire"),
        ("First assistant", "First assistant "),
        ("Second assistant", "Second assistant "),
        ("4th Official", "4th Official"),
    )

    nfixture = models.ForeignKey(
        NFixture, on_delete=models.CASCADE, null=True, blank=True
    )
    official = models.ForeignKey(
        Official, on_delete=models.CASCADE, null=True, blank=True
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture


class NMatchEvent(models.Model):
    nmatch = models.ForeignKey(NFixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("Goal", "Goal"),
        ("Assist", "Assist"),
        ("Foul", "Foul"),
        ("Interception", "Interception"),
        ("Penalty Shot", "Penalty Shot"),
        ("Turnover", "Turnover"),
        ("Rebound", "Rebound"),
        ("Obstruction", "Obstruction"),
        ("Contact", "Contact"),
        ("Short Pass", "Short Pass"),
        ("Long Pass", "Long Pass"),
        ("Center Pass", "Center Pass"),
        ("Timeout", "Timeout"),
        # Add more choices as needed
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )  # Example: "Card", "Corner", "Foul", "Assist"
    nteam = models.ForeignKey(Team, related_name="nteam", on_delete=models.CASCADE)
    athlete = models.ForeignKey(
        Athlete,
        related_name="nathlete",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    minute = models.IntegerField()
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.event_type} at {self.minute}'"

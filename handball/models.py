# models.py
from django.db import models
from athletes.models import Age, Athlete, Team
from accounts.models import Sport

# import uuid
from venues.models import Venue
from officials.models import Official
from accounts.models import Championship


# Create your models here.
class HCompetition(models.Model):
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


class HSeason(models.Model):
    hcompetition = models.ForeignKey(HCompetition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    participants = models.IntegerField()
    groups = models.IntegerField()
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    hteams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class HGroup(models.Model):
    hseason = models.ForeignKey(HSeason, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hteams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class HFixture(models.Model):
    statuses = (
        ("Pending", "Pending"),
        ("InPlay", "InPlay"),
        ("Complete", "Complete"),
        ("Postponed", "Postponed"),
    )

    stages = (("Group", "Group"), ("Knockout", "Knockout"))
    hseason = models.ForeignKey(
        HSeason, on_delete=models.CASCADE, null=True, blank=True
    )
    hcompetition = models.ForeignKey(
        HCompetition, on_delete=models.CASCADE, null=True, blank=True
    )
    stage = models.CharField(choices=stages, max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=statuses, max_length=100, null=True, blank=True, default="Pending"
    )
    round = models.CharField(max_length=100, null=True, blank=True)
    hgroup = models.ForeignKey(HGroup, on_delete=models.CASCADE, null=True, blank=True)

    # Use UUIDField for match_number

    venue = models.ForeignKey(
        Venue, related_name="hvenue", on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateTimeField(null=True, blank=True)
    team1 = models.ForeignKey(Team, related_name="hteam1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="hteam2", on_delete=models.CASCADE)
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    # Additional fields for Handball-specific scores
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

    hfixture = models.ForeignKey(
        HFixture, on_delete=models.CASCADE, null=True, blank=True
    )
    hofficial = models.ForeignKey(
        Official,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="hofficial",
    )
    match_role = models.CharField(choices=role, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fixture


class HMatchEvent(models.Model):
    hmatch = models.ForeignKey(HFixture, on_delete=models.CASCADE)
    EVENT_CHOICES = [
        ("Goal", "Goal"),  # Represents a successful goal
        ("PenaltyScore", "Penalty Score"),  # Represents a successful penalty shot
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
    )  # Example: "Goal", "PenaltyScore", "FreeThrow", "Steal"
    team = models.ForeignKey(Team, related_name="hteam", on_delete=models.CASCADE)
    athlete = models.ForeignKey(
        Athlete,
        related_name="hathlete",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    minute = models.IntegerField()
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.event_type} at {self.minute}'"

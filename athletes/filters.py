import django_filters
from .models import *
from .models import Athlete  # ,Team


class AthleteFilter(django_filters.FilterSet):
    class Meta:
        model = Athlete
        fields = ("name", "sport", "age", "gender")


class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = ("school", "sport", "gender", "age")

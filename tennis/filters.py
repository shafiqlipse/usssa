import django_filters
from .models import *


class CompetitionFilter(django_filters.FilterSet):
    class Meta:
        model = Competition
        fields = ("name", "sport", "age", "gender", "championship", "comcat")

class SeasonFilter(django_filters.FilterSet):
    class Meta:
        model = Season
        fields = {
            "name": ["exact", "icontains"],
            "competition": ["exact"],
            "participants": ["exact"],
            "start_date": ["exact"],
            "end_date": ["exact"],
        }

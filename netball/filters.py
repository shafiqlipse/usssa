import django_filters
from .models import *


class CompetitionFilter(django_filters.FilterSet):
    class Meta:
        model = NCompetition
        fields = ("name", "sport", "age", "gender", "championship", "comcat")

class SeasonFilter(django_filters.FilterSet):
    class Meta:
        model = NSeason
        fields = {
            "name": ["exact", "icontains"],
            "ncompetition": ["exact"],
            "participants": ["exact"],
            "start_date": ["exact"],
            "end_date": ["exact"],
        }

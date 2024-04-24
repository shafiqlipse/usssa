import django_filters
from .models import *


class CompetitionFilter(django_filters.FilterSet):
    class Meta:
        model = HCompetition
        fields = ("name", "sport", "age", "gender", "championship", "comcat")

class SeasonFilter(django_filters.FilterSet):
    class Meta:
        model = HSeason
        fields = {
            "name": ["exact", "icontains"],
            "hcompetition": ["exact"],
            "participants": ["exact"],
            "start_date": ["exact"],
            "end_date": ["exact"],
        }

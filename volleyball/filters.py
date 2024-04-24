import django_filters
from .models import *


class CompetitionFilter(django_filters.FilterSet):
    class Meta:
        model = VCompetition
        fields = ("name", "sport", "age", "gender", "championship", "comcat")

class SeasonFilter(django_filters.FilterSet):
    class Meta:
        model = VSeason
        fields = {
            "name": ["exact", "icontains"],
            "vcompetition": ["exact"],
            "participants": ["exact"],
            "start_date": ["exact"],
            "end_date": ["exact"],
        }

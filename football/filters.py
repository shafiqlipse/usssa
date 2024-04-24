import django_filters
from .models import *


class CompetitionFilter(django_filters.FilterSet):
    class Meta:
        model = Competition
        fields = (
            "name",
            "sport",
            "age",
            "gender",
            "championship",
            "season",
            "participants",
            "comcat",
        )


class SeasonFilter(django_filters.FilterSet):
    class Meta:
        model = Season
        fields = {
            "name": ["exact", "icontains"],
            "championship": ["exact"],
            "start_date": ["exact"],
            "end_date": ["exact"],
        }

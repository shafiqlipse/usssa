import django_filters
from .models import *


class CompetitionFilter(django_filters.FilterSet):
    class Meta:
        model = B5Competition
        fields = ("name", "sport", "age", "gender", "championship", "comcat")

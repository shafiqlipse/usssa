import django_filters
from .models import *


class OfficialFilter(django_filters.FilterSet):
    class Meta:
        model = Official
        fields = ("fname", "sport", "gender", "role")

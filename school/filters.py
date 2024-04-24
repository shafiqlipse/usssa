import django_filters

from .models import *
from .models import school_official


class OfficialFilter(django_filters.FilterSet):
    class Meta:
        model = school_official
        fields = ("name",  "gender", "role")

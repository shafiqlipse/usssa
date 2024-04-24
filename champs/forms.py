from django import forms
from accounts.models import Championship
from football.models import Season


class ChampionshipForm(forms.ModelForm):

    class Meta:
        model = Championship
        fields = [
            "name",
            "thumbnail",
        ]


class SeasonForm(forms.ModelForm):

    class Meta:
        model = Season
        fields = [
            "championship",
            "host",
            "name",
            "start_date",
            "end_date",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "gdate_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

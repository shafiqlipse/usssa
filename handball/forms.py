from django import forms
from .models import HCompetition
from athletes.models import Team
from .models import HSeason, HGroup
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = HCompetition
        fields = ["name", "age", "championship", "comcat", "gender"]


class HSeasonForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = HSeason
        fields = [
            "name",
            "hcompetition",
            "participants",
            "groups",
            "start_date",
            "end_date",
            "hteams",
        ]


class HGroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = HGroup
        fields = ["name", "hteams"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Override the 'teams' field to be empty initially
    #     self.fields["teams"].queryset = self.fields["teams"].queryset.none()


HGroupFormSet = forms.inlineformset_factory(
    parent_model=HSeason,
    model=HGroup,
    fields=["name", "hteams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting groups, set this to True
)

from django_select2 import forms as s2forms
from .models import HFixture, match_official, HMatchEvent

# from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = HFixture
        fields = [
            "stage",
            "status",
            "round",
            "hgroup",
            "venue",
            "date",
            "team1",
            "team2",
            "team1_score",
            "team2_score",
        ]
        widgets = {"group": forms.Select(attrs={"class": "select2"})}


class MatchOfficialForm(forms.ModelForm):
    class Meta:
        model = match_official
        fields = "__all__"
        widgets = {
            "match_role": s2forms.Select2Widget,
        }


class MatchEventForm(forms.ModelForm):
    class Meta:
        model = HMatchEvent
        fields = "__all__"
        widgets = {
            "event_type": s2forms.Select2Widget,
            "team": s2forms.Select2Widget,
            "athlete": s2forms.Select2Widget,
        }

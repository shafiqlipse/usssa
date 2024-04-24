from django import forms
from .models import NCompetition
from athletes.models import Team
from .models import NSeason, NGroup
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = NCompetition
        fields = ["name", "age", "championship", "comcat", "gender"]


class SeasonForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = NSeason
        fields = [
            "name",
            "ncompetition",
            "participants",
            "groups",
            "start_date",
            "end_date",
            "nteams",
        ]


class GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = NGroup
        fields = ["name", "nteams"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Override the 'teams' field to be empty initially
    #     self.fields["teams"].queryset = self.fields["teams"].queryset.none()


GroupFormSet = forms.inlineformset_factory(
    parent_model=NSeason,
    model=NGroup,
    fields=["name", "nteams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting groups, set this to True
)

from django_select2 import forms as s2forms
from .models import NFixture, Nmatch_official, NMatchEvent

# from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = NFixture
        fields = [
            "stage",
            "status",
            "round",
            "ngroup",
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
        model = Nmatch_official
        fields = "__all__"
        widgets = {
            "match_role": s2forms.Select2Widget,
        }


class MatchEventForm(forms.ModelForm):
    class Meta:
        model = NMatchEvent
        fields = "__all__"
        widgets = {
            "event_type": s2forms.Select2Widget,
            "nteam": s2forms.Select2Widget,
            "athlete": s2forms.Select2Widget,
        }

from django import forms
from .models import VCompetition
from athletes.models import Team
from .models import VSeason, VGroup
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = VCompetition
        fields = ["name", "age", "championship", "comcat", "gender"]


class SeasonForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = VSeason
        fields = [
            "name",
            "vcompetition",
            "participants",
            "groups",
            "start_date",
            "end_date",
            "teams",
        ]


class GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = VGroup
        fields = ["name", "vteams"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Override the 'teams' field to be empty initially
    #     self.fields["teams"].queryset = self.fields["teams"].queryset.none()


GroupFormSet = forms.inlineformset_factory(
    parent_model=VSeason,
    model=VGroup,
    fields=["name", "vteams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting vgroups, set this to True
)

from django_select2 import forms as s2forms
from .models import VFixture, Vmatch_official, VMatchEvent

# from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = VFixture
        fields = [
            "stage",
            "status",
            "round",
            "vgroup",
            "venue",
            "date",
            "team1",
            "team2",
            "set1_score",
            "set2_score",
            "set3_score",
        ]
        widgets = {"vgroup": forms.Select(attrs={"class": "select2"})}


class MatchOfficialForm(forms.ModelForm):
    class Meta:
        model = Vmatch_official
        fields = "__all__"
        widgets = {
            "match_role": s2forms.Select2Widget,
        }


class MatchEventForm(forms.ModelForm):
    class Meta:
        model = VMatchEvent
        fields = "__all__"
        widgets = {
            "event_type": s2forms.Select2Widget,
            "team": s2forms.Select2Widget,
            "athlete": s2forms.Select2Widget,
        }

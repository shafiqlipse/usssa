from django import forms
from .models import B5Competition
from athletes.models import Team
from .models import B5Season, B5Group
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = B5Competition
        fields = ["name", "age","season", "championship", "comcat", "gender"]




class B5GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = B5Group
        fields = ["name", "b5teams"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Override the 'teams' field to be empty initially
    #     self.fields["teams"].queryset = self.fields["teams"].queryset.none()


B5GroupFormSet = forms.inlineformset_factory(
    parent_model=B5Season,
    model=B5Group,
    fields=["name", "b5teams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting groups, set this to True
)

from django_select2 import forms as s2forms
from .models import B5Fixture, match_official, B5MatchEvent

# from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = B5Fixture
        fields = [
            "stage",
            "status",
            "round",
            "b5group",
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
        model = B5MatchEvent
        fields = "__all__"
        widgets = {
            "event_type": s2forms.Select2Widget,
            "team": s2forms.Select2Widget,
            "athlete": s2forms.Select2Widget,
        }

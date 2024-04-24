from django import forms
from .models import B3Competition
from athletes.models import Team
from .models import B3Competition, B3Group
from django.forms import CheckboxSelectMultiple


class CompForm(forms.ModelForm):
    class Meta:
        model = B3Competition
        fields = ["name", "age", "championship", "comcat", "gender"]





class B3GroupForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Replace Team with your actual model name
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = B3Group
        fields = ["name", "b3teams"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Override the 'teams' field to be empty initially
    #     self.fields["teams"].queryset = self.fields["teams"].queryset.none()


B3GroupFormSet = forms.inlineformset_factory(
    parent_model=B3Competition,
    model=B3Group,
    fields=["name", "b3teams"],
    extra=0,  # Set this to the number of forms you want initially
    can_delete=False,  # If you want to allow deleting groups, set this to True
)

from django_select2 import forms as s2forms
from .models import B3Fixture, match_official, B3MatchEvent

# from django.forms import TimeInput


class FixtureForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    # time = forms.TimeField(widget=TimeInput(attrs={"type": "time"}))

    class Meta:
        model = B3Fixture
        fields = "__all__"
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
        model = B3MatchEvent
        fields = "__all__"
        widgets = {
            "event_type": s2forms.Select2Widget,
            "team": s2forms.Select2Widget,
            "athlete": s2forms.Select2Widget,
        }

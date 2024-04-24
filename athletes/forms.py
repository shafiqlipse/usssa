from django import forms
from .models import *


class NewAthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = [
            "name",
            "lin",
            "sport",
            "date_of_birth",
            "gender",
            "classroom",
            "age",
            "photo",
            "Parent_fname",
            "Parent_lname",
            "parent_email",
            "parent_phone_number",
            "parent_nin",
            "parent_gender",
            "address",
            "relationship",
        ]


class UpdateAthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = ["name", "gender", "photo"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
       
            "sport",
            "gender",
            "age",
            "athletes",
            "official",
        ]
        widgets = {
            "athletes": forms.CheckboxSelectMultiple,
        }

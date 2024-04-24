from django import forms
from .models import *


class OfficerForm(forms.ModelForm):
    class Meta:
        model = Official
        fields = [
            "fname",
            "lname",
            "nin",
            "bio",
            "sport",
            "photo",
            "phone_number",
            "email",
            "gender",
            "role",
        ]

    widgets = {
        "date_of_birth": forms.DateInput(attrs={"type": "date"}),
       # "sport": forms(attrs={"class": "form-control"}),
    }

    def __init__(self, *args, **kwargs):
        super(OfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"

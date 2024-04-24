from django import forms
from .models import school_official, School


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "school_name",
            "EMIS",
            "badge",
            "region",
            "district",
            "zone",
            "fname",
            "lname",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["badge"].widget.attrs["onchange"] = "displayImage(this);"


class OfficialForm(forms.ModelForm):
    class Meta:
        model = school_official
        fields = [
            "name",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
            "role",
        ]

    widgets = {
        "date_of_birth": forms.DateInput(attrs={"type": "date"}),
    }

    def __init__(self, *args, **kwargs):
        super(OfficialForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"

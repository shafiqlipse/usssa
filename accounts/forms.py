from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import User
from django.core.validators import RegexValidator
from .models import User, Region, Zone

class SchoolRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "username",
            "password1",
            "password2",
            "is_school",
        ]

# class PasswordResetForm(forms.Form):
#     new_password1 = forms.CharField(widget=forms.PasswordInput())
#     new_password2 = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         fields = ["new_password1", "new_password2"]

# # from select2.forms import Select2Widget




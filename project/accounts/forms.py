"""Forms for accounts app"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ProfileDataModel


class CreateUserForm(UserCreationForm):
    """
    Form for user creation
    """

    class Meta:
        """Meta class for CreateUserForm"""

        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileDataForm(forms.ModelForm):
    """
    Profile model
    """

    last_name = forms.CharField(required=False)
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
    )
    profileimg = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        """Meta class for ProfileDataForm"""

        model = ProfileDataModel
        fields = ["first_name", "last_name", "bio", "profileimg"]

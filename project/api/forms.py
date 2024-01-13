from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        """Meta class for CreateUserForm"""

        model = User
        fields = ["username", "password"]

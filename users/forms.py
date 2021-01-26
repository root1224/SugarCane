"""User forms."""

# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Models
from django.contrib.auth.models import User
from users.models import Profile


class UserForm(forms.ModelForm):
    """User detail form."""
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')

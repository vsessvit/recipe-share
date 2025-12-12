"""
Forms for user authentication
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """
    Extended user registration form with email
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling to all form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        # Provide user-friendly help text
        self.fields["username"].help_text = (
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )
        self.fields["password1"].help_text = (
            "Your password must contain at least 8 characters."
        )

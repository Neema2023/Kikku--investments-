from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):

    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your full name",
        }),
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+250...",
        }),
    )

    referral_code_input = forms.CharField(
        required=False,
        label="Referral Code (optional)",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter referral code",
        }),
    )

    class Meta:
        model = CustomUser

        fields = [
            "full_name",
            "phone_number",
            "password1",
            "password2",
            "referral_code_input",
        ]

        widgets = {
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

        labels = {
            "password1": "Password",
            "password2": "Confirm Password",
        }

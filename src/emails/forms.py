from django import forms

from . import css


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email-login-input",
                "class": css.EMAIL_FIELD_CSS,
                "placeholder": "your email login",
            }
        )
    )


def clean_email(self):
    email = self.cleaned_data.get("email")
    return email

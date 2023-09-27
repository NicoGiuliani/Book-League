from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import CustomUser


User = get_user_model()


class UserSignupForm(UserCreationForm):
    username = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control text-center",
            }
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control text-center",
            }
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control text-center",
            }
        ),
    )
    email = forms.EmailField(
        label="",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control text-center",
            }
        ),
    )
    password1 = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control text-center",
            }
        ),
    )
    password2 = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": "form-control text-center",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    readonly_fields = ("last_login", "groups", "date_joined", "user_permissions")


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
    
    username = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control text-center",
                
            }
        ),
    )
    password = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control text-center",
            }
        ),
    )
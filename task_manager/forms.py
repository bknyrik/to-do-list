from django.contrib.auth.forms import BaseUserCreationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model


class RegisterUserForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class StaffChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"

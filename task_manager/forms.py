from django.contrib.auth.forms import (
    BaseUserCreationForm,
    UserChangeForm as DjangoUserChangeForm
)
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


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")

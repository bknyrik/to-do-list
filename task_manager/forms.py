from django.contrib.auth.forms import BaseUserCreationForm
from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("content", "deadline", "tags")


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


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class StaffChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"

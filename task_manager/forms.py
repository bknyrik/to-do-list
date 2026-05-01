from datetime import datetime

from django.contrib.auth.forms import BaseUserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from task_manager.models import Task


class TaskForm(forms.ModelForm):

    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Task
        fields = ("content", "deadline", "tags")

    def clean_deadline(self) -> datetime:
        deadline = self.cleaned_data.get("deadline")

        if deadline and self.instance.created_at > deadline:
            raise ValidationError("Deadline mustn't have past date and time")

        return deadline


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

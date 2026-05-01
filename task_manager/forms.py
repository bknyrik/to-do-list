from datetime import datetime

from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm
)
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from task_manager.models import Task, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

    def clean_name(self) -> str:
        name = self.cleaned_data["name"]

        if name != name.lower():
            raise ValidationError("Name must contain only lower letters")

        return name


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


class UserRegistrationForm(DjangoUserCreationForm):
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


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class StaffChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )

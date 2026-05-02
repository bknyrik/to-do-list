from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.models import Tag
from task_manager.forms import (
    TagForm,
    TaskForm,
    UserRegistrationForm,
    UserCreationForm,
    UserChangeForm,
)


class FormTests(TestCase):

    def test_tag_form_is_valid(self) -> None:
        data = {"name": "test_tag"}
        form = TagForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], data["name"])

    def test_task_form_is_valid(self) -> None:
        tag = Tag.objects.create(name="test_tag")
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        data = {
            "content": "Test content",
            "deadline": datetime.now(),
            "completed": True,
            "tags": (tag.id, )
        }
        form = TaskForm(data=data)
        form.instance.user = user

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["content"], data["content"])
        self.assertEqual(form.cleaned_data["deadline"], data["deadline"])
        self.assertEqual(form.cleaned_data["completed"], data["completed"])

    def test_user_registration_form_is_valid(self) -> None:
        data = {
            "username": "testuser",
            "first_name": "Test first",
            "last_name": "Test last",
            "email": "test@test.test",
            "password1": "testpass1234",
            "password2": "testpass1234",
        }

        form = UserRegistrationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["username"], data["username"])
        self.assertEqual(form.data["first_name"], data["first_name"])
        self.assertEqual(form.data["last_name"], data["last_name"])
        self.assertEqual(form.data["email"], data["email"])
        self.assertEqual(form.data["password1"], data["password1"])
        self.assertEqual(form.data["password2"], data["password2"])

    def test_user_creation_form_is_valid(self) -> None:
        data = {
            "username": "testuser",
            "first_name": "Test first",
            "last_name": "Test last",
            "email": "test@test.test",
            "password1": "passuser",
            "password2": "passuser",
            "is_superuser": True,
            "is_staff": True,
            "user_permissions": (1, 2)
        }

        form = UserCreationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["is_staff"], data["is_staff"])
        self.assertEqual(form.data["is_superuser"], data["is_superuser"])
        self.assertEqual(form.data["user_permissions"], data["user_permissions"])

    def test_user_change_form_is_valid(self) -> None:
        data = {
            "username": "testuser",
            "first_name": "Test first",
            "email": "test@test.test",
        }

        form = UserChangeForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["first_name"], data["first_name"])
        self.assertEqual(form.data["email"], data["email"])

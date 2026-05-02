from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.models import Tag, Task


HTTP_200_OK = 200
HTTP_403_FORBIDDEN = 403

TAG_LIST_URL = reverse("task_manager:tag-list")
TAG_CREATE_URL = reverse("task_manager:tag-create")
TAG_UPDATE_URL = reverse(
    "task_manager:tag-update",
    kwargs={"slug": "test_tag"}
)
TAG_DELETE_URL = reverse(
    "task_manager:tag-delete",
    kwargs={"slug": "test_tag"}
)
TASK_LIST_URL = reverse("task_manager:task-list")
USER_CREATE_URL = reverse("task_manager:user-create")


class UnauthorizedTests(TestCase):

    def test_tag_list_login_required(self) -> None:
        response = self.client.get(TAG_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

    def test_task_list_login_required(self) -> None:
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

    def test_register_user(self) -> None:
        data = {
            "username": "testuser",
            "password1": "testpass",
            "password2": "testpass",
        }

        self.client.post(USER_CREATE_URL, data=data)
        user = get_user_model().objects.get(username=data["username"])
        self.assertTrue(user.check_password(data["password1"]))


class AuthorizedUserTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(user=self.user)

    def test_tag_list(self) -> None:
        tag = Tag.objects.create(name="test_tag")
        response = self.client.get(TAG_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(tag, response.context["tag_list"])

    def test_tag_create_forbidden(self) -> None:
        response = self.client.get(TAG_CREATE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_tag_update_forbidden(self) -> None:
        response = self.client.get(TAG_UPDATE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_tag_delete_forbidden(self) -> None:
        response = self.client.get(TAG_DELETE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_task_list(self) -> None:
        task = Task.objects.create(
            content="Test content",
            completed=True,
            user=self.user
        )
        task.tags.set((Tag.objects.create(name="test_tag").id, ))
        response = self.client.get(TASK_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(task, response.context["task_list"])

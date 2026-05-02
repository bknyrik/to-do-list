from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.models import Tag, Task


User = get_user_model()

HTTP_200_OK = 200
HTTP_302_FOUND = 302
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
TASK_CREATE_URL = reverse("task_manager:task-create")
USER_CREATE_URL = reverse("task_manager:user-create")


class UnauthorizedTests(TestCase):

    def test_tag_list_login_required(self) -> None:
        response = self.client.get(TAG_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

    def test_task_list_login_required(self) -> None:
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

    def test_register_user_and_is_logged_in(self) -> None:
        data = {
            "username": "testuser",
            "password1": "testpass1234",
            "password2": "testpass1234",
        }
        response = self.client.post(USER_CREATE_URL, data=data)

        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertRedirects(response, TASK_LIST_URL)

        self.assertTrue(User.objects.filter(username=data["username"]).exists())
        user = User.objects.get(username=data["username"])

        self.assertTrue(user.check_password(data["password1"]))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)


class AuthorizedUserTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.tag = Tag.objects.create(name="test_tag")
        self.task = Task.objects.create(
            content="Test content",
            user=self.user
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
        response = self.client.get(TASK_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(self.task, response.context["task_list"])
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_task_list_completed(self) -> None:
        response = self.client.post(TASK_LIST_URL, data={"task_pk": self.task.id})
        test_task = Task.objects.first()

        self.assertTrue(test_task.completed)
        self.assertRedirects(response, TASK_LIST_URL)

    def test_task_create(self) -> None:
        tag = Tag.objects.create(name="test")
        data = {
            "content": "Test",
            "completed": True,
            "tags": (tag.id, )
        }

        self.client.post(TASK_CREATE_URL, data=data)
        task = Task.objects.first()

        self.assertEqual(task.user, self.user)
        self.assertIn(tag, task.tags.all())

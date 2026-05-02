from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


HTTP_200_OK = 200
HTTP_403_OK = 403

TAG_LIST_URL = reverse("task_manager:tag-list")
TAG_CREATE_URL = reverse("task_manager:tag-create")
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

    def test_tag_create_forbidden(self) -> None:
        response = self.client.get(TAG_CREATE_URL)
        self.assertEqual(response.status_code, HTTP_403_OK)

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
TASK_UPDATE_URL = reverse(
    "task_manager:task-update",
    kwargs={"slug": "test-content"}
)
TASK_DELETE_URL = reverse(
    "task_manager:task-delete",
    kwargs={"slug": "test-content"}
)
USER_CREATE_URL = reverse("task_manager:user-create")
USER_LIST_URL = reverse("task_manager:user-list")
USER_UPDATE_URL = reverse(
    "task_manager:user-update",
    kwargs={"slug": "testuser"}
)
USER_DELETE_URL = reverse(
    "task_manager:user-delete",
    kwargs={"slug": "testuser"}
)


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
        self.task.tags.set((self.tag, ))
        self.client.force_login(user=self.user)

    def test_tag_list(self) -> None:
        response = self.client.get(TAG_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(self.tag, response.context["tag_list"])

    def test_tag_create_forbidden(self) -> None:
        response = self.client.get(TAG_CREATE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertTemplateUsed(response, "403.html")

    def test_tag_update_forbidden(self) -> None:
        response = self.client.get(TAG_UPDATE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertTemplateUsed(response, "403.html")

    def test_tag_delete_forbidden(self) -> None:
        response = self.client.get(TAG_DELETE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertTemplateUsed(response, "403.html")

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
        data = {
            "content": "Test",
            "completed": True,
            "tags": (self.tag.id, )
        }

        response = self.client.post(TASK_CREATE_URL, data=data)
        task = Task.objects.get(content=data["content"])

        self.assertEqual(task.user, self.user)
        self.assertIn(self.tag, task.tags.all())
        self.assertRedirects(response, TASK_LIST_URL)

    def test_task_update(self) -> None:
        data = {
            "content": "New test content",
            "completed": True,
            "tags": (self.tag.id, )
        }
        response = self.client.post(TASK_UPDATE_URL, data=data)
        task = Task.objects.first()

        self.assertEqual(task.content, data["content"])
        self.assertEqual(task.completed, data["completed"])
        self.assertRedirects(response, TASK_LIST_URL)

    def test_task_delete(self) -> None:
        response = self.client.post(TASK_DELETE_URL)
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, TASK_LIST_URL)

    def test_user_list_forbidden(self) -> None:
        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertTemplateUsed(response, "403.html")

    def test_user_create_forbidden(self) -> None:
        response = self.client.get(USER_CREATE_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertTemplateUsed(response, "403.html")

    def test_user_update_current_user(self) -> None:
        data = {
            "username": "test_user_1",
            "email": "user1@test.test",
        }
        response = self.client.post(USER_UPDATE_URL, data=data)
        user = User.objects.get(username=data["username"])

        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])

        UPDATED_USER_UPDATE_URL = reverse(
            "task_manager:user-update",
            kwargs={"slug": user.slug}
        )

        self.assertRedirects(response, UPDATED_USER_UPDATE_URL)

    def test_user_update_another_user_forbidden(self) -> None:
        user = User.objects.create_user(
            username="test_user_2",
            password="testpass12345"
        )
        ANOTHER_USER_UPDATE_URL = reverse(
            "task_manager:user-update",
            kwargs={"slug": user.slug}
        )
        response = self.client.post(ANOTHER_USER_UPDATE_URL)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertTemplateUsed(response, "403.html")

    def test_user_delete_current_user(self) -> None:
        response = self.client.post(USER_DELETE_URL)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, HTTP_302_FOUND)

    def test_user_delete_another_user_forbidden(self) -> None:
        user = User.objects.create_user(
            username="test_user_2",
            password="testpass12345"
        )
        ANOTHER_USER_DELETE_URL = reverse(
            "task_manager:user-delete",
            kwargs={"slug": user.slug}
        )
        response = self.client.post(ANOTHER_USER_DELETE_URL)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)
        self.assertTemplateUsed(response, "403.html")


class AuthorizedAdminTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="testadmin",
            password="admin12345"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="password12345"
        )
        self.tag = Tag.objects.create(name="test_tag")
        self.client.force_login(user=self.admin_user)

    def test_tag_create(self) -> None:
        data = {"name": "test_tag_2"}
        response = self.client.post(TAG_CREATE_URL, data=data)
        tag = Tag.objects.get(name=data["name"])

        self.assertEqual(tag.name, data["name"])
        self.assertRedirects(response, TAG_LIST_URL)

    def test_tag_update(self) -> None:
        data = {"name": "testtag"}
        response = self.client.post(TAG_UPDATE_URL, data=data)
        tag = Tag.objects.first()

        self.assertEqual(tag.name, data["name"])
        self.assertRedirects(response, TAG_LIST_URL)

    def test_tag_delete(self) -> None:
        response = self.client.post(TAG_DELETE_URL)
        self.assertEqual(Tag.objects.count(), 0)
        self.assertRedirects(response, TAG_LIST_URL)

    def test_create_user(self) -> None:
        data = {
            "username": "testuser2",
            "password1": "testpass1234",
            "password2": "testpass1234",
            "is_staff": True,
        }
        response = self.client.post(USER_CREATE_URL, data=data)
        user = User.objects.get(username=data["username"])

        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.is_staff, data["is_staff"])
        self.assertTrue(user.check_password(data["password1"]))
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertRedirects(response, TASK_LIST_URL)

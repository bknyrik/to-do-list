from django.test import TestCase
from django.urls import reverse


HTTP_200_OK = 200

TAG_LIST_URL = reverse("task_manager:tag-list")
TASK_LIST_URL = reverse("task_manager:task-list")


class UnauthorizedTests(TestCase):

    def test_tag_list_login_required(self) -> None:
        response = self.client.get(TAG_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

    def test_task_list_login_required(self) -> None:
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

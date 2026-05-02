from django.test import TestCase
from django.urls import reverse


HTTP_200_OK = 200

TAG_LIST_URL = reverse("task_manager:tag-list")


class UnauthorizedTests(TestCase):

    def test_tag_list_login_required(self) -> None:
        response = self.client.get(TAG_LIST_URL)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

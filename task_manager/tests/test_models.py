from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.models import Tag, Task


class ModelTests(TestCase):

    def test_tag_str(self) -> None:
        test_tag = Tag.objects.create(name="test_tag")
        self.assertEqual(str(test_tag), "test_tag")

    def test_task_str(self) -> None:
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass12345"
        )
        task = Task.objects.create(
            content="Test content",
            user=user
        )
        self.assertEqual(
            str(task),
            f"Test content {datetime.now()} {task.has_done}"
        )

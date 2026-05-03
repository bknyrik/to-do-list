from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.models import Tag, Task


class ModelTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass12345"
        )

    def test_tag_str(self) -> None:
        test_tag = Tag.objects.create(name="test_tag")
        self.assertEqual(str(test_tag), "test_tag")

    def test_task_str(self) -> None:
        task = Task.objects.create(
            content="Test content",
            user=self.user
        )
        self.assertEqual(
            str(task),
            f"Test content {datetime.now()} {task.has_done}"
        )

    def test_task_has_done(self) -> None:
        task_1 = Task.objects.create(
            content="Task has done",
            completed=True,
            user=self.user
        )
        task_2 = Task.objects.create(
            content="Task hasn't done",
            user=self.user
        )

        self.assertEqual(task_1.has_done, "Done")
        self.assertEqual(task_2.has_done, "Not done")

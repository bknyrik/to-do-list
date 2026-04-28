from django.test import TestCase

from task_manager.models import Tag


class ModelTests(TestCase):

    def test_tag_str(self) -> None:
        test_tag = Tag.objects.create(name="test_tag")
        self.assertEqual(str(test_tag), "test_tag")

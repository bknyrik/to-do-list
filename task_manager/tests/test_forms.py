from django.test import TestCase

from task_manager.models import Tag
from task_manager.forms import TagForm


class FormTests(TestCase):

    def test_tag_form_is_valid(self) -> None:
        data = {"name": "test_tag"}
        form = TagForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], data["name"])

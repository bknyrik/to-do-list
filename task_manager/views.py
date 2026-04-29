from django.views import generic

from task_manager.models import Tag


class TagListView(generic.ListView):
    model = Tag

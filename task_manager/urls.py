from django.urls import path

from task_manager.views import (
    TagListView,
    TagCreateView,
)


urlpatterns = [
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
]

app_name = "task_manager"

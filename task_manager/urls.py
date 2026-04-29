from django.urls import path

from task_manager.views import (
    TagListView,
)


urlpatterns = [
    path("tags/", TagListView.as_view(), name="tag-list"),
]

app_name = "task_manager"

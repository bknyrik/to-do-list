from django.urls import path

from task_manager.views import (
    TagListView,
    TagCreateView,
    TagUpdateView
)


urlpatterns = [
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
]

app_name = "task_manager"

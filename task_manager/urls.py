from django.urls import path

from task_manager.views import (
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    RegisterUserView,
    UpdateUserView,
    DeleteUserView
)


urlpatterns = [
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
    path("", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("users/register/", RegisterUserView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", UpdateUserView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", DeleteUserView.as_view(), name="user-delete"),
]

app_name = "task_manager"

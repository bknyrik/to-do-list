from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

from task_manager.models import Tag, Task


class TagListView(generic.ListView):
    model = Tag


class TagCreateView(generic.CreateView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


class TaskListView(generic.ListView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class UserDetailView(generic.DetailView):
    model = get_user_model()


class RegisterUserView(generic.CreateView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:task-list")


class UpdateUserView(generic.UpdateView):
    model = get_user_model()

    def get_success_url(self) -> str:
        return reverse("task_manger:user-detail", args=(self.object.id,))


class DeleteUserView(generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:task-list")

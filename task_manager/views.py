from django.http import HttpRequest, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.contrib.auth import mixins

from task_manager.models import Tag, Task


class TagListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Tag


class TagCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.prefetch_related("tags")

    def get_queryset(self) -> QuerySet[Task]:
        return self.queryset.filter(user=self.request.user)

    def post(
        self,
        request: HttpRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirect:
        task_pk = request.POST.get("task_pk")

        if task_pk:
            task = Task.objects.get(pk=int(task_pk))
            task.completed = not task.completed
            task.save()

        return HttpResponseRedirect(reverse("task_manager:task-list"), *args, **kwargs)


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class RegisterUserView(generic.CreateView):
    model = get_user_model()
    fields = ("username", "first_name", "last_name", "email", "password")
    success_url = reverse_lazy("task_manager:task-list")


class UpdateUserView(generic.UpdateView):
    model = get_user_model()
    fields = ("username", "first_name", "last_name", "email")

    def get_success_url(self) -> str:
        return reverse("task_manger:user-detail", args=(self.object.id,))


class DeleteUserView(generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:task-list")

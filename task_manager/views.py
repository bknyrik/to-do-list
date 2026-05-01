from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.contrib.auth import mixins
from django.contrib.auth.forms import BaseUserCreationForm

from task_manager.models import Tag, Task
from task_manager.forms import (
    TagForm,
    TaskForm,
    RegisterUserForm,
    UserCreationForm,
    StaffChangeForm,
    UserChangeForm
)


class TagListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10


class TagCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


class TaskListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.prefetch_related("tags")
    paginate_by = 5

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


class TaskCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")

    def form_valid(self, form: TaskForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")

    def form_valid(self, form: TaskForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class UserListView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.ListView
):
    model = get_user_model()
    paginate_by = 10

    def has_permission(self) -> bool:
        return self.request.user.is_staff


class RegisterUserView(mixins.PermissionRequiredMixin, generic.CreateView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:task-list")

    def get_form_class(self) -> type[BaseUserCreationForm]:
        if self.request.user.is_anonymous:
            return RegisterUserForm

        return UserCreationForm

    def has_permission(self) -> bool:
        return self.request.user.is_staff or self.request.user.is_anonymous


class UserUpdateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.UpdateView
):
    model = get_user_model()

    def get_form_class(self) -> type:
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return StaffChangeForm

        return UserChangeForm

    def has_permission(self) -> bool:
        return (
            self.request.user.is_staff or
            self.request.user.id == self.get_object().id
        )

    def get_success_url(self) -> str:
        return reverse("task_manager:user-update", args=(self.object.id,))


class UserDeleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.DeleteView
):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:task-list")

    def has_permission(self) -> bool:
        return (
            self.request.user.is_staff or
            self.request.user.id == self.get_object().id
        )

from __future__ import annotations

from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin.filters import SimpleListFilter

from task_manager.models import Tag, Task


class HasDoneListFilter(SimpleListFilter):
    title = "status"
    parameter_name = "status"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: TaskAdmin
    ) -> tuple[tuple[str, str], ...]:
        return (
            ("0", "Not done"),
            ("1", "Done")
        )

    def queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Task]
    ) -> QuerySet[Task]:
        if self.value():
            return queryset.filter(completed=int(self.value()))

        return queryset


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    empty_value_display = "Absent"
    list_display = (
        "content",
        "created_at",
        "deadline",
        "get_status",
        "get_tags",
    )
    list_filter = (HasDoneListFilter,)

    @admin.display(description="Status")
    def get_status(self, task: Task) -> str:
        return task.has_done

    @admin.display(description="Tags")
    def get_tags(self, task: Task) -> str:
        return ", ".join(map(str, task.tags.all()))


class TaskInLine(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    empty_value_display = "Absent"
    add_fieldsets = (
        DjangoUserAdmin.add_fieldsets +
        (
            (
                "Additional info",
                {"fields": ("first_name", "last_name", "email")}
            ),
        )
    )
    inlines = (TaskInLine, )


admin.site.register(Tag)

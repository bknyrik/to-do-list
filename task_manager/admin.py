from __future__ import annotations

from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib import admin
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
    list_filter = (HasDoneListFilter, "tags")

    @admin.display(description="Status")
    def get_status(self, task: Task) -> str:
        return task.has_done

    @admin.display(description="Tags")
    def get_tags(self, task: Task) -> str:
        return ", ".join(map(str, task.tags.all()))


admin.site.register(Tag)

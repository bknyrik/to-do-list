from django.contrib import admin

from task_manager.models import Tag, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    empty_value_display = "Absent"
    list_display = (
        "content",
        "created_at",
        "deadline",
        "get_status",
    )

    @admin.display(description="Status")
    def get_status(self, task: Task) -> str:
        return task.has_done


admin.site.register(Tag)

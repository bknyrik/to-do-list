from django.db import models
from django.db.models import Q, F, constraints


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = ("-completed", "-created_at")
        constraints = (
            constraints.CheckConstraint(
                condition=Q(deadline__is_null=False)
                & Q(created_at__gte=F("deadline")),
                name="created_at_gte_deadline"
            ),
        )

    @property
    def has_done(self) -> str:
        return "Done" if self.completed else "Not done"

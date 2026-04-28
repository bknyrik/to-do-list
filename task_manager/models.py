from django.db import models
from django.db.models import Q, F, constraints, functions
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ("name", )
        constraints = (
            constraints.CheckConstraint(
                condition=Q(name=functions.Lower(F("name"))),
                name="name_lower"
            ),
        )

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-completed", "-created_at")
        constraints = (
            constraints.CheckConstraint(
                condition=Q(deadline__isnull=False)
                & Q(created_at__lte=F("deadline")),
                name="created_at_lte_deadline"
            ),
        )

    @property
    def has_done(self) -> str:
        return "Done" if self.completed else "Not done"

    def __str__(self) -> str:
        return f"{self.content} {self.created_at} {self.has_done}"


class User(AbstractUser):
    ...

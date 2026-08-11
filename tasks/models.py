from django.db import models
from django.conf import settings
from projects.models import Project

# Create your models here.

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = "tasks")
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    status = models.CharField(max_length = 20, choices = Status.choices, default = Status.TODO)
    priority = models.CharField(max_length = 20, choices = Priority.choices, default = Priority.MEDIUM)
    due_date = models.DateField(null = True, blank = True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null = True, blank = True, related_name = "assigned_tasks")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "created_tasks")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("project", "title")

    def __str__(self):
        return f"{self.title} ({self.project.name})"


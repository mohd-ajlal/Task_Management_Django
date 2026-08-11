from datetime import datetime
from rest_framework import serializers
from .models import Task
from projects.models import Project

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description", "status", "priority",
            "due_date", "assignee", "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def validate_due_date(self, value):
        if value and value < datetime.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate(self, attrs):
        project = attrs.get("project") or getattr(self.instance, "project", None)
        title = attrs.get("title") or getattr(self.instance, "title", None)

        qs = Task.objects.filter(project=project, title=title)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A task with this title already exists in the project.")
        return attrs

    def validate_project(self, project):
        request = self.context["request"]
        if request.user not in project.members.all():
            raise serializers.ValidationError(
                "You must be a member of this project to create tasks in it."
            )
        return project

    def validate_assignee(self, assignee):
        if assignee and self.instance and assignee not in self.instance.project.members.all():
            raise serializers.ValidationError(
                "Assignee must be a member of the project."
            )
        return assignee

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context["request"]
        if instance.created_by != request.user:
            raise serializers.ValidationError("You do not have permission to update this task.")
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["project"] = {
            "id": instance.project.id,
            "name": instance.project.name,
        }
        if instance.assignee:
            representation["assignee"] = {
                "id": instance.assignee.id,
                "username": instance.assignee.username,
            }
        else:
            representation["assignee"] = None
        return representation

    def validate_status(self, value):
        if value not in [choice[0] for choice in Task.Status.choices]:
            raise serializers.ValidationError("Invalid status value.")
        return value

    def validate_priority(self, value):
        if value not in [choice[0] for choice in Task.Priority.choices]:
            raise serializers.ValidationError("Invalid priority value.")
        return value

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
        
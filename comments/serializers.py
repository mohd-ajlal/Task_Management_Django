from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = ["id", "task", "author", "text", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["author"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context["request"]
        if instance.author != request.user:
            raise serializers.ValidationError("You do not have permission to update this comment.")
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = {
            "id": instance.author.id,
            "username": instance.author.username,
            "email": instance.author.email,
        }
        return representation

    def validate(self, attrs):
        request = self.context["request"]
        if request.method in ["PUT", "PATCH"]:
            if attrs.get("author") and attrs["author"] != request.user:
                raise serializers.ValidationError("You cannot change the author of the comment.")
        return attrs

    def validate_task(self, task):
        request = self.context["request"]
        if request.user not in task.project.members.all():
            raise serializers.ValidationError(
                "You must be a member of the project to comment on its tasks."
            )
        return task

    
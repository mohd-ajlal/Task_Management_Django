from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    
    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "members",
            "created_at", "updated_at"]
        read_only_fields = [ "owner","members", "created_at", "updated_at"]

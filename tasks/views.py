from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsProjectMember
from .filters import TaskFilter

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Task.objects.filter(project__members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

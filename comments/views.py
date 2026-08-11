from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentAuthorOrReadOnly

# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrReadOnly]
    filterset_fields = ["task"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        return Comment.objects.filter(task__project__members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

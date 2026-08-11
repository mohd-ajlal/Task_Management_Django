from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Generic reusable check: only the object's `owner` field can write."""

    def has_object_permission(self, request, view, obj):
        # Read permissions
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
from rest_framework import permissions

class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.members.all()
        return obj.owner_id == request.user.id
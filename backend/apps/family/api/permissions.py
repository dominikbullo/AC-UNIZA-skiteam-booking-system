from rest_framework import permissions


class IsOwnFamilyOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

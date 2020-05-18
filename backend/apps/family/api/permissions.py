from rest_framework import permissions


class IsOwnFamilyOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # FIXME
        return True

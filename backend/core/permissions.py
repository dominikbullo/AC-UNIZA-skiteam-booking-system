from rest_framework import permissions

from core import choices


class IsCoachOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return request.user.is_coach() or request.user.is_admin()

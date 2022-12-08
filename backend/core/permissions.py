from rest_framework import permissions


class IsCoachOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        # TODO: If A'AnonymousUser'
        try:
            return request.user.is_coach() or request.user.is_admin()
        except Exception as e:
            print(e)

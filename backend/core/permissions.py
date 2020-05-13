from rest_framework import permissions

from core import choices


class IsCoachOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        isCoach = request.user.profile.user_role == choices.UserTypeChoices.COACH
        isAdmin = request.user.profile.user_role == choices.UserTypeChoices.ADMIN

        print("Allow {user} view {view} -> {allow}".format(user=request.user, view=str(view),
                                                           allow=isCoach or isAdmin))
        return isCoach or isAdmin

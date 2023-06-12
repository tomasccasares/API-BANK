from rest_framework.permissions import BasePermission

from api import constants, models


class IsAdmin(BasePermission):
    message = "User is not admin"

    def has_permission(self, request, view):
        if not request.user.groups.exists():
            return False
        
        return request.user.groups.all()[0].name == constants.GROUP_ADMIN

class IsUser(BasePermission):
    message = "The user does not have the user role."

    def has_permission(self, request, view):
        if not request.user.groups.exists():
            return False
        
        return request.user.groups.all()[0].name == constants.GROUP_USER

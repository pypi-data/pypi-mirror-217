from rest_framework import permissions


class ExamplePermissions:
    class CanAccessView(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):

            return False

        def has_permission(self, request, view):

            return True


class GeneralPermissions:
    class IsService(permissions.BasePermission):
        """if request is made from a service

        Args:
            permissions (_type_): _description_
        """

        def has_object_permission(self, request, view, obj):

            return False

        def has_permission(self, request, view):

            return True

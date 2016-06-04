from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserModelPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # Just browsing.
            return True
        else:
            # User is trying to edit!
            if not request.user.is_authenticated():
                # Not authorized. Nope!
                return False

            if obj.pk != request.user.pk:
                # Not my object. Nope!
                return False

            return True


class TaskModelPermission(BasePermission):
    def has_permission(self, request, view):
        # TODO
        return True

    def has_object_permission(self, request, view, obj):
        # TODO
        return True


class CallModelPermission(BasePermission):
    def has_permission(self, request, view):
        # TODO
        return True

    def has_object_permission(self, request, view, obj):
        # TODO
        return True


class BadgeModelPermission(BasePermission):
    def has_permission(self, request, view):
        # TODO
        return True

    def has_object_permission(self, request, view, obj):
        # TODO
        return True


class UserBadgeModelPermission(BasePermission):
    def has_permission(self, request, view):
        # TODO
        return True

    def has_object_permission(self, request, view, obj):
        # TODO
        return True
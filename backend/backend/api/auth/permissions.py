from rest_framework.permissions import IsAuthenticated, BasePermission


class OwnerPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.warehouse == request.user.sewing_workshop.warehouse


class DirectorPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.role.DIRECTOR


class IsVerifiedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified

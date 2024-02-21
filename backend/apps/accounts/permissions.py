from rest_framework.permissions import IsAuthenticated


class OwnerPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.warehouse == request.user.sewing_workshop.warehouse


class DirectorPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.role in ["DIRECTOR"]


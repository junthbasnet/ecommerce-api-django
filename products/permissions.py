from rest_framework import permissions
from .utils import get_ordered_product_obj

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of a review
        # ordered_product_id = request.data.get('ordered_product_id')
        # ordered_product_obj = get_ordered_product_obj(ordered_product_id)
        # return ordered_product_obj.user == request.user == obj.user and ordered_product_obj.reviews == obj
        return request.user == obj.user


class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
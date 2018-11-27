from rest_framework import permissions

from cashes.apis.backends import IamPortAPI


class IsAuthenticatedWithPurchase(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        유저가 인증되지 않았을 시 환불하기 위한 Permissions
        """
        is_authenticated = request.user and request.user.is_authenticated
        if is_authenticated is False:
            IamPortAPI().purchase_cancel(request.data['response']['imp_uid'])
        return is_authenticated

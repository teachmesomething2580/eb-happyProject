from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from cashes.apis.backends import IamPortAPI
from cashes.apis.pagination import CashResultSetPagination
from cashes.apis.permissions import IsAuthenticatedWithPurchase
from giftcard.apis.serializer import GiftCardTypeSerializer, EmailOrderGiftCardSerializer, \
    SMSOrderGiftCardSerializer, AddressOrderGiftCardSerializer, OrderGiftCardSerializer
from giftcard.models import GiftCardType, OrderGiftCard


class GiftCardTypeListAPIView(generics.ListAPIView):
    queryset = GiftCardType.objects.all()
    serializer_class = GiftCardTypeSerializer


class OrderGiftCardPurchaseView(APIView):
    permission_classes = (
        IsAuthenticatedWithPurchase,
    )

    def post(self, request):
        # 필수로 가져와야하는 항목을 가져온다.
        imp_uid = request.data['imp_uid']
        try:
            merchant_uid = request.data['merchant_uid']
            paid_amount = request.data['paid_amount']
        except KeyError:
            IamPortAPI().purchase_cancel(imp_uid)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # IamPort의 access_token을 생성하고 위변조를 검사한다.
        result = IamPortAPI().inquiry_purchase_info(imp_uid, paid_amount)
        result_status = result['status']

        if result_status == 'success':
            purchase = request.data['purchase']
            delivery_type = purchase['delivery_type']
            purchase_list = purchase['purchase_list']

            if delivery_type == 'email':
                serializer_class = EmailOrderGiftCardSerializer
                extra_field = 'email'
            elif delivery_type == 'sms':
                serializer_class = SMSOrderGiftCardSerializer
                extra_field = 'phone'
            elif delivery_type == 'address':
                serializer_class = AddressOrderGiftCardSerializer
                extra_field = ''
                # 추후 변경성
            else:
                return

            # 객체 생성
            order = OrderGiftCard.create_order(serializer_class, extra_field, imp_uid, merchant_uid, purchase_list, request.user)
            serializer = serializer_class(order, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 위변조시
            error_res = {
                'error': result
            }
            IamPortAPI().purchase_cancel(imp_uid)
            return Response(error_res, status=status.HTTP_400_BAD_REQUEST)


class OrderGiftCardListView(generics.ListAPIView):
    queryset = OrderGiftCard.objects.all()
    serializer_class = OrderGiftCardSerializer
    pagination_class = CashResultSetPagination
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)

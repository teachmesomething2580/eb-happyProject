import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from cashes.apis.backends import IamPortAPI
from cashes.apis.permissions import IsAuthenticatedWithPurchase
from giftcard.apis.filters import OrderGiftCardFilter
from giftcard.apis.pagination import OrderGiftCardPagination
from giftcard.apis.serializer import GiftCardTypeSerializer, OrderGiftCardSerializer, HappyGiftCardSerializer, \
    OrderGiftCardWithPINSerializer, PINGiftCardSerializer
from giftcard.models import GiftCardType, OrderGiftCard, HappyGiftCard, PINGiftCard


class GiftCardTypeListAPIView(generics.ListAPIView):
    queryset = GiftCardType.objects.all().select_related('mall_category')
    serializer_class = GiftCardTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_hotdeal', )


class HappyGiftCardListAPIView(generics.ListAPIView):
    queryset = HappyGiftCard.objects.all()
    serializer_class = HappyGiftCardSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('delivery_type', )


class PINGiftCardPurchaseView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        try:
            PINGiftCardList = request.data['PINGiftCardList']
        except KeyError:
            raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})

        exst_PINGiftCardList = []

        for PIN in PINGiftCardList:
            try:
                PIN_number = PIN.get('PIN')

                if PIN_number == '':
                    continue

                created_at = datetime.datetime.strptime(PIN.get('created_at'), '%Y-%m-%d')

            except KeyError:
                raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})
            except ValueError:
                raise serializers.ValidationError({'detail': '정확한 발행일을 입력해주세요.'})

            try:
                p = PINGiftCard.objects.get(PIN=PIN_number, is_used=False, created_at=created_at)
                if p:
                    exst_PINGiftCardList.append(p)
            except PINGiftCard.DoesNotExist:
                continue

        if exst_PINGiftCardList.__len__() == 0:
            raise serializers.ValidationError({'detail': '유효한 상품이 없습니다.'})

        status, merchant_uid, full_amount = PINGiftCard.PINCardToHappyCash(exst_PINGiftCardList, request.user)

        if status is True:
            serializer = PINGiftCardSerializer(exst_PINGiftCardList, many=True)
            return_datas = {
                'datas': serializer.data,
                'merchant_uid': merchant_uid,
                'full_amount': full_amount,
            }
            return Response(return_datas)
        else:
            raise serializers.ValidationError({'detail': '결제 정보 생성시 오류가 발생했습니다.'})


class BeforeOrderGiftCardPurchaseView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        try:
            paid_amount = request.data['paid_amount']
            purchase = request.data['purchase']
            delivery_type = purchase['delivery_type']
            purchase_list = purchase['purchase_list']
        except KeyError:
            raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})

        full_amount = 0
        is_happyCash = False

        for p in purchase_list:
            for price in p['giftcard_info']:
                amount = price['amount']
                if amount == '':
                    amount = 0
                g = HappyGiftCard.objects.get(gift_card_unique_id=price['type'])
                if g is None:
                    raise serializers.ValidationError({'detail': '해당 GiftCard 종류가 존재하지 않습니다.'})
                full_amount += g.price * int(amount)

        if full_amount != paid_amount:
            raise serializers.ValidationError({'detail': '값이 변조되었습니다.'})
        elif full_amount == 0:
            raise serializers.ValidationError({'detail': '생성할 상품권이 존재하지 않습니다.'})

        if delivery_type == 'email':
            extra_field = 'email'
        elif delivery_type == 'sms':
            extra_field = 'sms'
        elif delivery_type == 'address':
            extra_field = ''
        else:
            raise serializers.ValidationError({'detail': '해당 배송방법이 존재하지 않습니다.'})

        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        merchant_uid = 'giftCard_' + str(timestamp)
        serializer_class = OrderGiftCardSerializer

        if request.data.get('is_happyCash'):
            is_happyCash = True

        create_status = OrderGiftCard.before_create_order(serializer_class, extra_field, merchant_uid, purchase_list,
                                           request.user, full_amount, is_happyCash)
        if create_status is not True:
            raise serializers.ValidationError({'detail': '결제 정보 생성시 오류가 발생했습니다.'})
        return Response({'merchant_uid': merchant_uid, 'full_amount': full_amount}, status=status.HTTP_201_CREATED)


class OrderGiftCardPurchaseView(APIView):
    permission_classes = (
        IsAuthenticatedWithPurchase,
    )

    def post(self, request):
        try:
            imp_uid = request.data.get('imp_uid')
        except KeyError:
            raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})
        try:
            merchant_uid = request.data['merchant_uid']
        except KeyError:
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '전달되지 않은 정보로 인해 결제가 취소됩니다.'})

        order_gift_card_list = OrderGiftCard.objects.filter(merchant_uid=merchant_uid, user=request.user)
        if not order_gift_card_list.exists():
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '결제 전 정보가 존재하지 않아 결제가 취소됩니다..'})

        # IampPort의 Access_Token을 생성하고 위변조를 검사한다.
        result = IamPortAPI().inquiry_purchase_info(imp_uid, order_gift_card_list[0].full_amount)
        result_status = result['status']

        if result_status == 'success':
            create_pin_status = OrderGiftCard.create_order(order_gift_card_list, imp_uid)
            if create_pin_status == True:
                serializer = OrderGiftCardSerializer(order_gift_card_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                IamPortAPI().purchase_cancel(imp_uid)
                raise serializers.ValidationError({'detail': '결제 정보 생성 중 오류가 발생하였습니다.'})
        else:
            IamPortAPI().purchase_cancel(imp_uid)
            raise serializers.ValidationError({'detail': '위 변조사항이 발생하였습니다.'})


class OrderGiftCardListView(generics.ListAPIView):
    queryset = OrderGiftCard.objects.all().distinct('merchant_uid')
    serializer_class = OrderGiftCardSerializer
    pagination_class = OrderGiftCardPagination
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = (DjangoFilterBackend, )
    filter_class = OrderGiftCardFilter

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(user=user)


class OrderGiftCardWithPINListView(generics.ListAPIView):
    queryset = PINGiftCard.objects.all()
    serializer_class = OrderGiftCardWithPINSerializer
    pagination_class = OrderGiftCardPagination
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related('created_in_order')
        return queryset.filter(created_in_order__order_gift_card__user=user,
                               created_in_order__order_gift_card__is_purchase=True,
                               created_in_order__order_gift_card__delivery_type=self.request.query_params.get('delivery_type'))

    def get_serializer_context(self):
        return {'delivery_type': self.request.query_params.get('delivery_type')}
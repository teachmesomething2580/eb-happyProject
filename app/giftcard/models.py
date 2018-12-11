import random
import string

from django.contrib.auth import get_user_model
from django.db import models, transaction
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers

from cashes.apis.backends import IamPortAPI
from cashes.models import Cash
from members.models import Address

User = get_user_model()


def increment_giftcard_cnt():
    last = GiftCardType.objects.last()
    if not last:
        return 'gcnt_0000'
    now = last.gift_card_unique_id
    gcnt, numbering = now.split('_')
    add_number = int(numbering) + 1
    return gcnt + '_' + f'{add_number:0>4}'


class GiftCardCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    shop_image = models.ImageField(
        upload_to='images/shop_image',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class GiftCardType(models.Model):
    CATEGORY_CHOICE = (
        ('h', 'hot'),
        ('m', 'mobile'),
    )

    gift_card_unique_id = models.CharField(max_length=8, default=increment_giftcard_cnt, editable=False)

    amount = models.IntegerField()
    is_hotdeal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICE,
    )
    mall_category = models.ForeignKey(
        GiftCardCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.mall_category.name) + ' ' + str(self.amount)+'원권'


class PINGiftCard(models.Model):
    PIN = models.CharField(
        max_length=30,
    )
    is_used = models.BooleanField(default=True)
    created_in_order = models.ForeignKey(
        'OrderGiftCardAmount',
        on_delete=models.CASCADE,
    )

    @staticmethod
    def create_pin():
        PIN = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))
        if PINGiftCard.objects.filter(PIN=PIN, is_used=False):
            return PINGiftCard.create_pin()
        return PIN


class OrderGiftCardAmount(models.Model):
    gift_card = models.ForeignKey(
        GiftCardType,
        on_delete=models.CASCADE,
    )
    order_gift_card = models.ForeignKey(
        'OrderGiftCard',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()


class OrderGiftCard(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        max_length=100,
    )
    before_purchase = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=15)

    @staticmethod
    @transaction.atomic
    def create_order(serializer_class, extra_field, imp_uid, merchant_uid, purchase_list, user, paid_amount):
        serializer_lists = []

        if imp_uid is None:
            if user.happy_cash <= paid_amount:
                raise serializers.ValidationError({'detail': '잔액이 모자랍니다.'})
            Cash.give_point(
                content=merchant_uid,
                amount=paid_amount,
                hammer_or_cash='hc',
                use_or_save='u',
                user=user,
            )

        # 여러 Email을 가지고 주문하였기 때문에
        for purchase in purchase_list:
            data = {
                'content': merchant_uid,
                'name': purchase['name'],
                extra_field: purchase[extra_field],
            }
            serializer = serializer_class(data=data)

            if serializer.is_valid():
                order_gift_card = serializer.save(user=user)
                for purchase_info in purchase['giftcard_info']:
                    # OrderGiftCardAmount 생성
                    amount = purchase_info['amount']
                    # GiftCard 가져옴
                    g = GiftCardType.objects.get(gift_card_unique_id=purchase_info['type'])
                    if g is None:
                        raise serializers.ValidationError({'detail': '해당 상품권의 종류가 없습니다.'})

                    o = OrderGiftCardAmount.objects.create(
                        gift_card=g,
                        order_gift_card=order_gift_card,
                        amount=amount
                    )

                    # PINGiftCard 생성
                    for i in amount:
                        PIN = PINGiftCard.create_pin()
                        PINGiftCard.objects.create(
                            PIN=PIN,
                            is_used=False,
                            created_in_order=o
                        )
                serializer_lists.append(order_gift_card)
            else:
                # serailizer 오류시
                if imp_uid:
                    IamPortAPI().purchase_cancel(imp_uid)
                    raise serializers.ValidationError({'detail': '결제 정보 생성시 오류가 발생했습니다.'})
        return serializer_lists


class EmailOrderGiftCard(OrderGiftCard):
    email = models.EmailField()


class SMSOrderGiftCard(OrderGiftCard):
    phone = PhoneNumberField()


class AddressOrderGiftCard(OrderGiftCard):
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
    )
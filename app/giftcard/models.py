import datetime
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


def increment_happycard_cnt():
    last = HappyGiftCard.objects.last()
    if not last:
        return 'gcnt_0000'
    now = last.gift_card_unique_id
    gcnt, numbering = now.split('_')
    add_number = int(numbering) + 1
    return gcnt + '_' + f'{add_number:0>4}'


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

    gift_card_unique_id = models.CharField(max_length=9, default=increment_giftcard_cnt, editable=False)

    amount = models.IntegerField()
    is_hotdeal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    category = models.CharField(
        max_length=2,
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
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.PIN

    @staticmethod
    @transaction.atomic
    def PINCardToHappyCash(exst_PINGiftCardList, user):
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        merchant_uid = 'happyCash_' + str(timestamp)
        full_amount = 0

        for PIN in exst_PINGiftCardList:
            price = PIN.created_in_order.gift_card.price
            full_amount += price
            PIN.is_used = True
            PIN.save()

        data = {
            'merchant_uid': merchant_uid,
            'amount': full_amount,
            'hammer_or_cash': 'hc',
            'use_or_save': 's',
        }

        Cash.give_point(
            user=user,
            **data
        )

        return True, merchant_uid, full_amount


    @staticmethod
    def create_pin():
        PIN = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))
        if PINGiftCard.objects.filter(PIN=PIN, is_used=False):
            return PINGiftCard.create_pin()
        return PIN


class HappyGiftCard(models.Model):
    DELIVERY_TYPE_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'EMAIL'),
        ('address', 'address'),
    )
    gift_card_unique_id = models.CharField(max_length=10, default=increment_happycard_cnt, editable=False)
    price = models.PositiveIntegerField()
    delivery_type = models.CharField(
        choices=DELIVERY_TYPE_CHOICES,
        max_length=10,
    )


class OrderGiftCardAmount(models.Model):
    gift_card = models.ForeignKey(
        HappyGiftCard,
        on_delete=models.CASCADE,
    )
    order_gift_card = models.ForeignKey(
        'OrderGiftCard',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()

    def __str__(self):
        return '상품권 가격: ' + str(self.gift_card.price) + ', 상품권 갯수 : ' + str(self.amount)


class OrderGiftCard(models.Model):
    DELIVERY_TYPE_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'EMAIL'),
        ('address', 'address'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    merchant_uid = models.CharField(
        max_length=100,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=15)
    is_purchase = models.BooleanField(default=False)
    full_amount = models.PositiveIntegerField()
    delivery_type = models.CharField(
        choices=DELIVERY_TYPE_CHOICES,
        max_length=10,
    )

    @staticmethod
    @transaction.atomic
    def before_create_order(serializer_class, extra_field, merchant_uid, purchase_list, user, full_amount, is_happyCash):
        if is_happyCash:
            data = {
                'merchant_uid': merchant_uid,
                'amount': full_amount,
                'hammer_or_cash': 'hc',
                'use_or_save': 'u',
            }

            Cash.give_point(
                user=user,
                **data
            )

        for purchase in purchase_list:
            data = {
                'merchant_uid': merchant_uid,
                'name': purchase['name'],
                extra_field: purchase['infoTo'],
                'full_amount': full_amount,
                'delivery_type': extra_field,
            }
            serializer = serializer_class(data=data)

            if serializer.is_valid():
                order_gift_card = serializer.save(user=user)
                for purchase_info in purchase['giftcard_info']:
                    # OrderGiftCardAmount 생성
                    amount = purchase_info['amount']
                    g = HappyGiftCard.objects.get(gift_card_unique_id=purchase_info['type'])
                    if g is None:
                        raise serializers.ValidationError({'detail': '해당 상품권의 종류가 없습니다.'})

                    OrderGiftCardAmount.objects.create(
                        gift_card=g,
                        order_gift_card=order_gift_card,
                        amount=amount
                    )

            else:
                raise serializers.ValidationError(serializer.errors)

        if is_happyCash:
            order_gift_card_list = OrderGiftCard.objects.filter(merchant_uid=merchant_uid, user=user)
            OrderGiftCard.create_order(order_gift_card_list, None)
        return True

    @staticmethod
    @transaction.atomic
    def create_order(order_gift_card_list, imp_uid):
        for order_gift_card in order_gift_card_list:
            order_list = order_gift_card.ordergiftcardamount_set.all()

            # 핀 생성
            for one_order in order_list:
                for _ in range(0, one_order.amount):
                    PIN = PINGiftCard.create_pin()
                    PINGiftCard.objects.create(
                        PIN=PIN,
                        is_used=False,
                        created_in_order=one_order
                    )

            # 결제 완료
            order_gift_card.is_purchase = True
            order_gift_card.save()
        return True


class EmailOrderGiftCard(OrderGiftCard):
    email = models.EmailField()


class SMSOrderGiftCard(OrderGiftCard):
    sms = PhoneNumberField()


class AddressOrderGiftCard(OrderGiftCard):
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
    )
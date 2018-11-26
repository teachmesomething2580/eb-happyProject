from rest_framework import generics

from giftcard.apis.serializer import GiftCardTypeSerializer
from giftcard.models import GiftCardType


class GiftCardTypeListAPIView(generics.ListAPIView):
    queryset = GiftCardType.objects.all()
    serializer_class = GiftCardTypeSerializer
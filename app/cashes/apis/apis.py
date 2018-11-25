from rest_framework import generics, permissions

from cashes.apis.serializer import CashPurchaseSerializer
from cashes.models import Cash


class CashPurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Cash.objects.all()
    serializer_class = CashPurchaseSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)

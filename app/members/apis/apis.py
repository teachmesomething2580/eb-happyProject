from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from members.apis.serializer import UserProfileSerializer, UserAuthTokenSerializer, UserCreateSerializer, \
    DeliverySerializer, RatingSerializer
from members.apis.permissions import IsUserAdmin
from members.models import Address, Rating

User = get_user_model()


class UserAuthTokenView(APIView):
    def post(self, request):
        serializer = UserAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListGenericAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsUserAdmin,
    )

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        fields = self.request.query_params.get('fields')
        if fields:
            kwargs['fields'] = fields.split(',')
        serializer = serializer_class(*args, **kwargs)
        return serializer


class UserRetrieveGenericAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        fields = self.request.query_params.get('fields')
        if fields:
            kwargs['fields'] = fields.split(',')
        serializer = serializer_class(*args, **kwargs)
        return serializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if lookup_url_kwarg not in self.kwargs:
            if not self.request.user.is_authenticated:
                raise NotAuthenticated()
            return self.request.user

        user = super().get_object()

        if self.request.user.is_staff is not True and self.request.user.pk is not user.pk:
            raise PermissionDenied()

        return user


class UserCreateGenericAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class DeliveryListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)


class RatingListGenericAPIView(generics.ListAPIView):
    """
    Rating List API
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsUserAdmin,
    )

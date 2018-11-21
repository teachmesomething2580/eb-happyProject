from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from members.apis.serializer import UserSerializer, UserAuthTokenSerializer
from members.permissions import IsUserAdmin

User = get_user_model()


class AuthTokenView(APIView):
    def post(self, request):
        serializer = UserAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListGenericAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
    serializer_class = UserSerializer

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

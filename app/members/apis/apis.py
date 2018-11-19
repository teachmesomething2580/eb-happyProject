from django.contrib.auth import get_user_model
from rest_framework import generics

from members.apis.serializer import UserSerializer

User = get_user_model()


class UserListGenericAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
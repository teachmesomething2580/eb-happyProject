from django.contrib.auth import get_user_model
from rest_framework import generics

from members.apis.serializer import UserSerializer

User = get_user_model()


class UserListGenericAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        fields = self.request.query_params.get('fields').split(',')
        kwargs['fields'] = fields
        serializer = serializer_class(*args, **kwargs)
        return serializer
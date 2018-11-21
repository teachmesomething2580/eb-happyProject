from django.contrib.auth import get_user_model
from rest_framework import serializers


class DynamicUserSerizlier(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """
        User 모델을 Dynamic하게 정보를 사용하기 위해 BaseSerializer를 작성
        """

        fields = kwargs.pop('fields', None)
        super(DynamicUserSerizlier, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicUserSerizlier):
    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'username',
            'phone',
            'email',
            'rating',
            'hammer',
            'happy_cash',
        )

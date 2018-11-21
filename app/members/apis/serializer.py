from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from members.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        exclude = (
            'rating_choices_name',
        )

    def get_name(self, obj):
        return obj.get_rating_choices_name_display()


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
    rating = RatingSerializer()

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
        depth = 1


class UserAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs['username'], password=attrs['password'])

        if not self.user:
            raise serializers.ValidationError('유저 정보가 잘못되었습니다.')
        return attrs

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        return {
            'token': token.key,
        }
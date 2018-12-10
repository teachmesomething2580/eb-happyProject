from django.contrib.auth import get_user_model, authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from members.models import Rating, Address

User = get_user_model()


class RatingSerializer(serializers.ModelSerializer):
    """
    Rating 정보들을 가져오기 위한 Serializer
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        exclude = (
            'rating_choices_name',
        )

    def get_name(self, obj):
        return obj.get_rating_choices_name_display()


class DynamicUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """
        User 모델을 Dynamic하게 정보를 사용하기 위해 BaseSerializer를 작성
        """

        fields = kwargs.pop('fields', None)
        super(DynamicUserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserProfileSerializer(DynamicUserSerializer):
    """
    유저 정보를 가져오기 위한 Serializer
    """
    rating = RatingSerializer()

    class Meta:
        model = User
        fields = (
            'name',
            'username',
            'phone',
            'email',
            'rating',
            'sns_agree',
            'email_agree',
            'hammer',
            'happy_cash',
        )

        read_only_fields = (
            'name',
            'username',
            'phone',
            'rating',
            'hammer',
            'happy_cash',
        )
        depth = 1


class UserAuthTokenSerializer(serializers.Serializer):
    """
    유저 토큰을 저장하기위한 Serializer
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs['username'], password=attrs['password'])

        if not self.user:
            raise serializers.ValidationError({'detail': '유저 정보가 잘못되었습니다.'})
        return attrs

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        return {
            'token': token.key,
        }


class CheckPasswordSerializer(serializers.Serializer):
    """
    패스워드 정보 확인
    """
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_authenticate = False

    def validate(self, attrs):
        username = self.context['request'].user.username

        user = authenticate(username=username, password=attrs['password'])

        if not user:
            raise serializers.ValidationError({'detail': '비밀번호가 잘못되었습니다.'})
        self.is_authenticate = True
        return attrs

    def to_representation(self, instance):
        return {
            'detail': '인증이 완료되었습니다.',
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """
    유저 생성을 위한 Serializer
    """
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'phone',
            'email',
            'birth',
            'name',
            'sns_agree',
            'email_agree',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def create(self, validated_data):
        self.user = User.normalManager.create_user(**validated_data)
        return self.user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        data.pop('sns_agree')
        data.pop('email_agree')
        token = Token.objects.get_or_create(user=self.user)[0]
        data['token'] = token.key
        return data


class DeliverySerializer(serializers.ModelSerializer):
    """
    배달 주소 정보 저장
    """
    class Meta:
        model = Address
        fields = (
            'postcode',
            'address',
            'detail',
            'user',
        )
        read_only_fields = (
            'user',
        )

    def create(self, validated_data):
        d, _ = Address.objects.get_or_create(**validated_data)
        return d
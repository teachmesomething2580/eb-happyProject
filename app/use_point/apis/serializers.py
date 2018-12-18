from rest_framework import serializers

from use_point.models import UsePoint, UsePointCategory


class UsePointLikeSerializer(serializers.Serializer):
    """
    좋아요 버튼에 대한 Serializer
    """
    usepoint_pk = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.usepoint = None

    def validate(self, attrs):
        if not UsePoint.objects.filter(pk=attrs['usepoint_pk']).exists():
            raise serializers.ValidationError({'detail': '입점몰 정보가 잘못되었습니다.'})

        self.usepoint = UsePoint.objects.get(pk=attrs['usepoint_pk'])

        return attrs

    def to_representation(self, instance):
        user = self.context['request'].user
        if self.usepoint.like_users.filter(pk=user.pk).exists():
            self.usepoint.like_users.remove(user)
            return {
                'status': 'deleted'
            }
        else:
            self.usepoint.like_users.add(user)
            return {
                'status': 'created'
            }


class CategorySerializer(serializers.ModelSerializer):
    """
    Usepoint Category List Serializer
    """
    class Meta:
        model = UsePointCategory
        fields = '__all__'


class UsePointSerializer(serializers.ModelSerializer):
    """
    UsePoint Serializer
    """
    is_liked = serializers.SerializerMethodField()
    like_users_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = None

    class Meta:
        model = UsePoint
        fields = (
            'id',
            'name',
            'category',
            'is_online',
            'where_to_use',
            'created_at',
            'site',
            'shop_image',
            'like_users_count',
            'is_liked',
        )
        depth = 1

    def get_is_liked(self, obj):
        return getattr(obj, 'is_like', False)

    def get_like_users_count(self, obj):
        return obj.like_users_count


class UsePointImportSerializer(serializers.ModelSerializer):
    """
    입점몰을 카테고리별로 나타내기위한 ListSerializer
    """
    class Meta:
        model = UsePoint
        fields = '__all__'


class CategoryUsePointSerializer(serializers.ModelSerializer):
    """
    입점몰의 카테고리별로 UsePoint를 나타냄
    """
    usepoint_set = UsePointImportSerializer(read_only=True, many=True)

    class Meta:
        model = UsePointCategory
        fields = (
            'name',
            'usepoint_set',
        )
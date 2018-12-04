from rest_framework import serializers

from use_point.models import UsePoint, UsePointCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsePointCategory
        fields = '__all__'


class UsePointSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    like_users_count = serializers.SerializerMethodField()

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
        request = self.context.get('request', None)
        if request:
            if obj.like_users.filter(pk=request.user.pk).exists():
                return True

        return False

    def get_like_users_count(self, obj):
        return obj.like_users_count


class UsePointImportListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_online=True, where_to_use__is_import_point=True)
        return super(UsePointImportListSerializer, self).to_representation(data)


class UsePointImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsePoint
        fields = '__all__'
        list_serializer_class = UsePointImportListSerializer


class CategoryUsePointSerializer(serializers.ModelSerializer):
    usepoint_set = UsePointImportSerializer(read_only=True, many=True)

    class Meta:
        model = UsePointCategory
        fields = (
            'name',
            'usepoint_set',
        )
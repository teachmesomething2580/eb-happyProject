from rest_framework import serializers

from use_point.models import UsePoint, UsePointCategory


class UsePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsePoint
        fields = '__all__'
        depth = 1


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
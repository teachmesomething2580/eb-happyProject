from rest_framework import serializers

from use_point.models import UsePoint, UsePointCategory


class UsePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsePoint
        fields = '__all__'
        depth = 1


class CategoryUsePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsePointCategory
        fields = (
            'name',
            'usepoint_set',
        )
        depth = 1
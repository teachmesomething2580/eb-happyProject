from rest_framework import serializers

from use_point.models import UsePoint


class UsePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsePoint
        fields = '__all__'
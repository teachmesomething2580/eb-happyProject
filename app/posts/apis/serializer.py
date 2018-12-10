from rest_framework import serializers

from posts.models import Notice, FAQ, Inquiry, FAQCategory, FAQSubCategory, NoticeCategory


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        depth = 1


class NoticeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeCategory
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        depth = 1


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = (
            'category',
            'user',
        )


class FAQSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQSubCategory
        exclude = (
            'main_category',
        )


class FAQCategorySerializer(serializers.ModelSerializer):
    sub_category = FAQSubCategorySerializer(many=True)

    class Meta:
        model = FAQCategory
        fields = (
            'name',
            'sub_category',
        )
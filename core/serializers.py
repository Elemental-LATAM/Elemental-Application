from rest_framework import serializers

class SkillsSerializer(serializers.Serializer):
    slug = serializers.CharField(read_only=True)
    category = serializers.CharField(required=False)
    name = serializers.CharField(required=False, allow_blank=True, max_length=30)
    quantity = serializers.CharField(default=0)
    top_category = serializers.BooleanField()


class InterestSerializer(serializers.Serializer):
    slug = serializers.CharField(read_only=True)
    category = serializers.CharField(required=False)
    name = serializers.CharField(required=False, allow_blank=True, max_length=30)
    quantity = serializers.CharField(default=0)
    top_category = serializers.BooleanField()

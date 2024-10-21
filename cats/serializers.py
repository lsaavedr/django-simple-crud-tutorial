# cats/serializers.py
from rest_framework import serializers

from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    """
    Cat Serializers
    """

    class Meta:
        model = Cat
        fields = "__all__"

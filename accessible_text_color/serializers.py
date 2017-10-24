from rest_framework.serializers import ModelSerializer
from accessible_text_color.calculator import Color


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ('rgb')

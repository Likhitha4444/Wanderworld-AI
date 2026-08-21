from rest_framework import serializers
from apps.images.models import DestinationImage, HotelImage, AttractionImage

class BaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ['id', 'image', 'alt_text', 'caption', 'display_order', 'is_primary']

class DestinationImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = DestinationImage

class HotelImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = HotelImage

class AttractionImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = AttractionImage

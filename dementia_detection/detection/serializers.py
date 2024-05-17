# detection/serializers.py

from rest_framework import serializers
from .models import DementiaImage

class DementiaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DementiaImage
        fields = ('id', 'image', 'prediction', 'uploaded_at')  # Đảm bảo trường uploaded_at được bao gồm

from rest_framework import serializers
from .models import GobiernoLocal




class GobiernoLocalSerializer(serializers.ModelSerializer):
    """Serializador del modelo Gobierno Local"""
    class Meta:
        model = GobiernoLocal
        fields = '__all__'

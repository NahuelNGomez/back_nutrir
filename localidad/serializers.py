from rest_framework import serializers
from .models import Localidad

class LocalidadSerializer(serializers.ModelSerializer):
    """Serializador del modelo Localidad"""
    class Meta:
        model = Localidad
        fields = '__all__'

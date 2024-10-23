from rest_framework import serializers
from .models import Provincia

class ProvinciaSerializer(serializers.ModelSerializer):
    """Serializador del modelo Provincia"""
    class Meta:
        model = Provincia
        fields = '__all__' #si quiero todos los campos


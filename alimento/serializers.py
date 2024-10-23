from rest_framework import serializers
from .models import Alimento, Unidad

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'

class AlimentoSerializer(serializers.ModelSerializer):
    unidades = UnidadSerializer(many=True, read_only=True)

    class Meta:
        model = Alimento
        fields = '__all__'

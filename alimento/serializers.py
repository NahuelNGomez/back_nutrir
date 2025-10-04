from rest_framework import serializers
from .models import Alimento, Unidad

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ['id', 'nombre', 'equivalencia_gramos', 'equivalencia_ml']
    
    def validate(self, data):
        """
        Validar que solo se puede especificar gramos o ml, no ambos
        """
        equivalencia_gramos = data.get('equivalencia_gramos')
        equivalencia_ml = data.get('equivalencia_ml')
        
        if equivalencia_gramos and equivalencia_ml:
            raise serializers.ValidationError(
                "No se puede especificar equivalencia en gramos y ml al mismo tiempo."
            )
        
        if not equivalencia_gramos and not equivalencia_ml:
            raise serializers.ValidationError(
                "Debe especificar equivalencia en gramos o ml."
            )
        
        return data

class AlimentoSerializer(serializers.ModelSerializer):
    unidades = UnidadSerializer(many=True, read_only=True)

    class Meta:
        model = Alimento
        fields = '__all__'

from rest_framework import serializers
from .models import Departamento


class DepartamentoSerializer(serializers.ModelSerializer):
    """Serializador del modelo Departamento"""
    class Meta:
        model = Departamento
        fields = '__all__' #si quiero todos los campos


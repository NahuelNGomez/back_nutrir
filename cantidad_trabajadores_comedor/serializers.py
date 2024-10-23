from rest_framework import serializers
from .models import CantidadTrabajadoresComedor


class CantidadTrabajadoresComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CantidadTrabajadoresComedor
        fields = '__all__' #si quiero todos los campos


from rest_framework import serializers
from .models import ServicioComedor


class ServicioComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServicioComedor
        fields = '__all__' #si quiero todos los campos


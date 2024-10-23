from rest_framework import serializers
from .models import FuenteAguaComedor


class FuenteAguaComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = FuenteAguaComedor
        fields = '__all__' #si quiero todos los campos


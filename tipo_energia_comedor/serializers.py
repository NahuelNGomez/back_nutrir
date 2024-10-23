from rest_framework import serializers
from .models import TipoEnergiaComedor


class TipoEnergiaComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoEnergiaComedor
        fields = '__all__' #si quiero todos los campos


from rest_framework import serializers
from .models import ActividadComplementariaComedor


class ActividadComplementariaComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActividadComplementariaComedor
        fields = '__all__' #si quiero todos los campos


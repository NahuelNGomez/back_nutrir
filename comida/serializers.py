from rest_framework import serializers
from .models import Comida


class ComidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comida
        fields = '__all__' #si quiero todos los campos


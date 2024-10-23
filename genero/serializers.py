from rest_framework import serializers
from .models import Genero


class GeneroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genero
        fields = '__all__' #si quiero todos los campos


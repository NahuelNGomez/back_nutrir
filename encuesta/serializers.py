from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Encuesta, AlimentoEncuesta, NoSeSirvioEncuesta
from comida.models import Comida


class EncuestaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encuesta
        fields = '__all__' #si quiero todos los campos

class AlimentoEncuestaCompletoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlimentoEncuesta
        fields = '__all__' #si quiero todos los campos

class AlimentoEncuestaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlimentoEncuesta
        fields = ['alimento', 'cantidad', 'unidad']
class ComidaEncuestaSerializer(serializers.Serializer):

	comida = PrimaryKeyRelatedField(queryset=Comida.objects.all())
	alimento = AlimentoEncuestaSerializer(many=True)

class ComidaEncuestaPostSerializer(serializers.Serializer):

	encuesta = EncuestaSerializer()
	comida1 = ComidaEncuestaSerializer()
	comida2 = ComidaEncuestaSerializer()
	comida3 = ComidaEncuestaSerializer()


class NoSeSirvioEncuestaSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoSeSirvioEncuesta
        fields = '__all__' #si quiero todos los campos


from rest_framework import serializers

class ComedorListaSerializer(serializers.Serializer):
	comedor = serializers.IntegerField()
	lista = serializers.ListField()

class ComedorListaLabelSerializer(serializers.Serializer):
	comedor = serializers.IntegerField()
	labels = serializers.ListField()
	lista = serializers.ListField()

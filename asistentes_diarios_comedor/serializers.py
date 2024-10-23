from rest_framework import serializers
from .models import AsistentesDiariosComedor


class AsistentesDiariosComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = AsistentesDiariosComedor
        fields = '__all__' #si quiero todos los campos


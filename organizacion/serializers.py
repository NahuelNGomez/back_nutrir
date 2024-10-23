from rest_framework import serializers
from .models import Organizacion


class OrganizacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organizacion
        fields = '__all__' #si quiero todos los campos


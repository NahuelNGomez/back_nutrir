from rest_framework import serializers
from .models import TipoOrganizacion


class TipoOrganizacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoOrganizacion
        fields = '__all__' #si quiero todos los campos


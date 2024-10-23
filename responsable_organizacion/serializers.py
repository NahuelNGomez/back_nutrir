from rest_framework import serializers
from .models import ResponsableOrganizacion


class ResponsableOrganizacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResponsableOrganizacion
        fields = '__all__' #si quiero todos los campos


from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import TipoOrganizacionSerializer
from .models import TipoOrganizacion


class TipoOrganizacionViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = TipoOrganizacionSerializer
    def get_queryset(self):
        return TipoOrganizacion.objects.all()


from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import ResponsableOrganizacionSerializer
from .models import ResponsableOrganizacion


class ResponsableOrganizacionViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = ResponsableOrganizacionSerializer
    def get_queryset(self):
        return ResponsableOrganizacion.objects.all()


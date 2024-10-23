from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import OrganizacionSerializer
from .models import Organizacion


class OrganizacionViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = OrganizacionSerializer
    def get_queryset(self):
        return Organizacion.objects.all()


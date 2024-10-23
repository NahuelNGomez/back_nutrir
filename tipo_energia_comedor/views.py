from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import TipoEnergiaComedorSerializer
from .models import TipoEnergiaComedor


class TipoEnergiaComedorViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = TipoEnergiaComedorSerializer
    def get_queryset(self):
        return TipoEnergiaComedor.objects.all()


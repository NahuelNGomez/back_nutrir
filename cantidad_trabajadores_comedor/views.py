from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import CantidadTrabajadoresComedorSerializer
from .models import CantidadTrabajadoresComedor


class CantidadTrabajadoresComedorViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = CantidadTrabajadoresComedorSerializer
    def get_queryset(self):
        return CantidadTrabajadoresComedor.objects.all()


from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import ServicioComedorSerializer
from .models import ServicioComedor


class ServicioComedorViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = ServicioComedorSerializer
    def get_queryset(self):
        return ServicioComedor.objects.all()


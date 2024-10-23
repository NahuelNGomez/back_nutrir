from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import FuenteAguaComedorSerializer
from .models import FuenteAguaComedor


class FuenteAguaComedorViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = FuenteAguaComedorSerializer
    def get_queryset(self):
        return FuenteAguaComedor.objects.all()


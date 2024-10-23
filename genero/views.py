from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import GeneroSerializer
from .models import Genero


class GeneroViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = GeneroSerializer
    def get_queryset(self):
        return Genero.objects.all()


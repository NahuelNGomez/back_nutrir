from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import ActividadComplementariaComedorSerializer
from .models import ActividadComplementariaComedor


class ActividadComplementariaComedorViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = ActividadComplementariaComedorSerializer
    def get_queryset(self):
        return ActividadComplementariaComedor.objects.all()


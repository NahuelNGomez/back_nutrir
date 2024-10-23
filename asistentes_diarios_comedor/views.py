from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import AsistentesDiariosComedorSerializer
from .models import AsistentesDiariosComedor


class AsistentesDiariosComedorViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = AsistentesDiariosComedorSerializer
    def get_queryset(self):
        return AsistentesDiariosComedor.objects.all()


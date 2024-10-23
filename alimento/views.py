from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .models import AlimentoSARA
from rest_framework.decorators import api_view
from .serializers import AlimentoSerializer, UnidadSerializer
from .models import Alimento, Unidad


class AlimentoViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = AlimentoSerializer
    def get_queryset(self):
        return Alimento.objects.all()
@api_view(['GET'])
def get_alimento_sara(request, alimento_id):
    try:
        alimento_sara = AlimentoSARA.objects.get(id=alimento_id)
        data = {
            'nombre': alimento_sara.nombre,
            'cantidad_porcion': alimento_sara.cantidad_porcion,
            'hidratos_carbono': alimento_sara.hidratos_carbono,
            'proteinas': alimento_sara.proteinas,
            'grasas': alimento_sara.grasas,
            'grasas_totales': alimento_sara.grasas_totales,
            'energia': alimento_sara.energia,
            'sodio': alimento_sara.sodio,
        }
        return Response(data, status=status.HTTP_200_OK)
    except AlimentoSARA.DoesNotExist:
        return Response({'error': 'Alimento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class UnidadesViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = UnidadSerializer
    def get_queryset(self):
        return Unidad.objects.all()

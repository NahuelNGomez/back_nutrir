from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .models import AlimentoSARA
from rest_framework.decorators import api_view
from .serializers import AlimentoSerializer, UnidadSerializer
from .models import Alimento, Unidad

# Import para autocompletado
from dal import autocomplete


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
            
            # Nutrientes básicos
            'agua': alimento_sara.agua,
            'energia': alimento_sara.energia,
            'proteinas': alimento_sara.proteinas,
            'lipidos': alimento_sara.lipidos,
            
            # Ácidos grasos
            'acidos_grasos_saturados': alimento_sara.acidos_grasos_saturados,
            'acidos_grasos_monoinsaturados': alimento_sara.acidos_grasos_monoinsaturados,
            'acidos_grasos_poliinsaturados': alimento_sara.acidos_grasos_poliinsaturados,
            'colesterol': alimento_sara.colesterol,
            
            # Carbohidratos y fibra
            'hidratos_carbono': alimento_sara.hidratos_carbono,
            'fibra': alimento_sara.fibra,
            'cenizas': alimento_sara.cenizas,
            
            # Minerales
            'sodio': alimento_sara.sodio,
            'potasio': alimento_sara.potasio,
            'calcio': alimento_sara.calcio,
            'fosforo': alimento_sara.fosforo,
            'hierro': alimento_sara.hierro,
            'zinc': alimento_sara.zinc,
            
            # Vitaminas
            'niacina': alimento_sara.niacina,
            'folatos': alimento_sara.folatos,
            'vitamina_a': alimento_sara.vitamina_a,
            'tiamina': alimento_sara.tiamina,
            'riboflavina': alimento_sara.riboflavina,
            'vitamina_b12': alimento_sara.vitamina_b12,
            'vitamina_c': alimento_sara.vitamina_c,
            'vitamina_d': alimento_sara.vitamina_d,
            
            # Campos legacy para compatibilidad
            'grasas': alimento_sara.grasas,
            'grasas_totales': alimento_sara.grasas_totales,
        }
        return Response(data, status=status.HTTP_200_OK)
    except AlimentoSARA.DoesNotExist:
        return Response({'error': 'Alimento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class UnidadesViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = UnidadSerializer
    def get_queryset(self):
        return Unidad.objects.all()


# Vista de autocompletado para AlimentoSARA
class AlimentoSARAAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # No mostrar resultados si el usuario no está autenticado
        if not self.request.user.is_authenticated:
            return AlimentoSARA.objects.none()
        
        qs = AlimentoSARA.objects.all().order_by('nombre')
        if self.q:  # Para que en el listado se pueda buscar por nombre del alimento
            qs = qs.filter(nombre__icontains=self.q)
        return qs

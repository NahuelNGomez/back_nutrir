from django.db.models import Value, F, CharField
from django.db.models.functions import Concat
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ComidaSerializer
from .models import Comida
from alimento.models import Alimento
from alimento.models import Unidad


class ComidaViewList(generics.ListAPIView):
    """Vista para que muestre el listado"""

    serializer_class = ComidaSerializer
    def get_queryset(self):
        return Comida.objects.all()

class ComidaAlimentoView(generics.ListAPIView):

    serializer_class = ComidaSerializer

    def list(self, request, *args, **kwargs):
        id = self.kwargs['id_c']
        comida = Comida.objects.get(id=id)
        host = request.get_host()

        alimentos = Alimento.objects.filter(id__in=comida.alimento.all()).values(
            'id', 'nombre', 'foto', 'cantidad_porcion', 'hidratos_carbono', 'proteinas', 'grasas', 'energia'
        )

        alimentos_extendidos = []
        for alimento in alimentos:
            unidades = Unidad.objects.filter(alimento=alimento['id']).values('id','nombre')
            unidades_extendidas = [{'id': unidad['id'], 'nombre': unidad['nombre']} for unidad in unidades]

            alimento_extendido = {
                'id': alimento['id'],
                'nombre': alimento['nombre'],
                'cantidad_porcion': alimento['cantidad_porcion'],
                'hidratos_carbono': alimento['hidratos_carbono'],
                'proteinas': alimento['proteinas'],
                'grasas': alimento['grasas'],
                'energia': alimento['energia'],
                'unidades': unidades_extendidas,
                'foto': 'http://'+host+'/media/' + alimento['foto'],
            }

            alimentos_extendidos.append(alimento_extendido)

        comida_extendida = {
            'id': id,
            'nombre': comida.nombre,
            'foto': 'http://'+host+'/media/'+str(comida.foto),
            'alimento': alimentos_extendidos,
            'horario': comida.horario,
        }

        return Response({'data': comida_extendida})

class ComidaServicioView(generics.ListAPIView):

	serializer_class = ComidaSerializer
	def list(self, request, *args, **kwargs):
		servicio = self.kwargs['servicio']
		host = request.get_host()

		if servicio == 'desayuno' or servicio == 'merienda':
			data = {
				'bebida': Comida.objects.filter(horario='desayuno_merienda_bebidas').values('id', 'nombre', 'horario').annotate(foto=Concat(Value('http://'+host+'/media/'), 'foto',  output_field=CharField())).order_by('nombre'),
				'comida': Comida.objects.filter(horario='desayuno_merienda_comida').values('id', 'nombre', 'horario').annotate(foto=Concat(Value('http://'+host+'/media/'), 'foto',  output_field=CharField())).order_by('nombre'),
			}
		elif servicio == 'cena' or servicio == 'almuerzo': # or servicio == 'olla_popular':
			data = {
				'entrada': Comida.objects.filter(horario='almuerzo_cena_entrada').values('id', 'nombre', 'horario').annotate(foto=Concat(Value('http://'+host+'/media/'), 'foto',  output_field=CharField())).order_by('nombre'),
				'plato principal': Comida.objects.filter(horario='almuerzo_cena_plato_principal').values('id', 'nombre', 'horario').annotate(foto=Concat(Value('http://'+host+'/media/'), 'foto',  output_field=CharField())).order_by('nombre'),
				'postre': Comida.objects.filter(horario='almuerzo_cena_postre').values('id', 'nombre', 'horario').annotate(foto=Concat(Value('http://'+host+'/media/'), 'foto',  output_field=CharField())).order_by('nombre')
			}
		return Response({'data': data})

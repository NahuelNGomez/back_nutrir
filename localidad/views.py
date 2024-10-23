from rest_framework import generics
from .serializers import LocalidadSerializer
from .models import Localidad


class Localidad_ID_GLDeptoProvinciaview(generics.ListAPIView):
   """Vista para que muestre las localidades segun el id de gobiernos locales, departamento y de la provincia"""
   serializer_class = LocalidadSerializer
   http_method_names = ['get']
   def get_queryset(self):
       id_p = self.kwargs['id_p']
       id_d= self.kwargs['id_d']
       id_gl = self.kwargs['id_gl']
       return Localidad.objects.filter(gobierno_local=id_gl, departamento=id_d, provincia=id_p)

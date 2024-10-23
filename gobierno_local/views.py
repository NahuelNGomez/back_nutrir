from django.shortcuts import render
from rest_framework import generics
from .serializers import GobiernoLocalSerializer
from .models import GobiernoLocal

class GobiernoLocalIDDeptoProvinciaview(generics.ListAPIView):
   """Vista para que muestre los gobiernos locales segun el id de un departamento y de la provincia"""
   serializer_class = GobiernoLocalSerializer
   http_method_names = ['get']
   def get_queryset(self):
       id_p = self.kwargs['id_p']
       id_d= self.kwargs['id_d']
       return GobiernoLocal.objects.filter(departamento=id_d, provincia=id_p)


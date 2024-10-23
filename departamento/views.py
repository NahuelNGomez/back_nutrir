from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import DepartamentoSerializer
from .models import Departamento



class DepartamentoIDProvinciaview(generics.ListAPIView):
   """Vista para que muestre los departamentos segun el id de una provincia """
   serializer_class = DepartamentoSerializer
   http_method_names = ['get']
   def get_queryset(self):
       id = self.kwargs['id']
       return Departamento.objects.filter(provincia=id)


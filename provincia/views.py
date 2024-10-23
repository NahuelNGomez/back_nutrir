from rest_framework import generics
from .serializers import ProvinciaSerializer
from .models import Provincia

class ProvinciaViewList(generics.ListAPIView):
    """Vista para que muestre el listado de provincias"""
    serializer_class = ProvinciaSerializer
    paginate_by = 10
    model= Provincia
    def get_queryset(self):
       return Provincia.objects.all()


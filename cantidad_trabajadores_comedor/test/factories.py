import factory
from cantidad_trabajadores_comedor.models import CantidadTrabajadoresComedor

class CantidadTrabajadoresComedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CantidadTrabajadoresComedor
    rango = factory.Faker('name')
    
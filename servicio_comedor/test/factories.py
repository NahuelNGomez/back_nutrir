import factory
from servicio_comedor.models import ServicioComedor

class ServicioComedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServicioComedor
    nombre = factory.Faker('name')
    
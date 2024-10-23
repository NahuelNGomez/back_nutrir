import factory
from actividad_complementaria_comedor.models import ActividadComplementariaComedor

class ActividadComplementariaComedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActividadComplementariaComedor
    nombre = factory.Faker('name')
    
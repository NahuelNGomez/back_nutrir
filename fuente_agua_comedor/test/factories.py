import factory
from fuente_agua_comedor.models import FuenteAguaComedor

class FuenteAguaComedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FuenteAguaComedor
    rango = factory.Faker('name')
    
import factory
from tipo_energia_comedor.models import TipoEnergiaComedor

class TipoEnergiaComedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TipoEnergiaComedor
    rango = factory.Faker('name')
    
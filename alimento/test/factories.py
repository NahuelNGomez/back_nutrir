import factory
from alimento.models import Alimento

class AlimentoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Alimento
    rango = factory.Faker('nombre')
    
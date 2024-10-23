import factory
from comida.models import Comida

class ComidaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comida
    rango = factory.Faker('nombre')
    
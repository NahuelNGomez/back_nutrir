import factory
from genero.models import Genero

class GeneroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genero
    nombre = factory.Faker('name')
    
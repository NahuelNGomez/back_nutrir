import factory
from provincia.models import Provincia

class ProvinciaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Provincia
    nombre = factory.Faker('country')
    codigo_UTA = factory.Faker('random_number',digits=2)

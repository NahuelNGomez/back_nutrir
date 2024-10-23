import factory
from provincia.test.factories import ProvinciaFactory
from departamento.test.factories import DepartamentoFactory
from gobierno_local.models import GobiernoLocal


class GobiernoLocalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = GobiernoLocal

    nombre = factory.Faker('city')
    tipo_gobierno =  factory.Faker('sentence')
    codigo_UTA = factory.Faker('random_number',digits=9)
    departamento =factory.SubFactory(DepartamentoFactory)
    provincia = factory.SubFactory(ProvinciaFactory)
    latitud = factory.Faker('latitude')
    longitud = factory.Faker('latitude')

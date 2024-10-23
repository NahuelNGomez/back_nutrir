import factory
from departamento.models import Departamento
from provincia.test.factories import ProvinciaFactory


class DepartamentoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Departamento
    nombre = factory.Faker('name')
    codigo_UTA = factory.Faker('random_number',digits=5)
    provincia = factory.SubFactory(ProvinciaFactory)

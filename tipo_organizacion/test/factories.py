import factory
from tipo_organizacion.models import TipoOrganizacion

class TipoOrganizacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TipoOrganizacion
    nombre = factory.Faker('name')
    
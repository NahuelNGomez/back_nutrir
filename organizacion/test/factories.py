import factory
from organizacion.models import Organizacion

class OrganizacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organizacion
    nombre = factory.Faker('name')
    
import factory
from organizacion.models import ResponsableOrganizacion

class ResponsableOrganizacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResponsableOrganizacion
    nombre = factory.Faker('name')
    
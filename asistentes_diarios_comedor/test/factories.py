import factory
from asistentes_diarios_comedor.models import AsistentesDiariosComedor

class AsistentesDiariosComedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AsistentesDiariosComedor
    rango = factory.Faker('name')
    
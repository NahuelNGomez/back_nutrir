from random import random

import factory
from user.models import UsuarioPersonalizado

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = UsuarioPersonalizado

    email= factory.Faker('email')
    password= factory.PostGenerationMethodCall('set_password', 'default_password')

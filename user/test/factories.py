from random import random

import factory
from user.models import UsuarioPersonalizado

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = UsuarioPersonalizado

    cuil= factory.Faker('word', ext_word_list=["27404554919", "20398340960", "2017443784", "20110137312", "27115158231", "20382517750","20267424161", "20404554922", "20398340982", "20398341016", "27398341029", "27398341039", "27398341049", "27398341059", "27398341069", "27398341079","27398341089","27398341099","27398341109","27398341119","27398341129"])
    email= factory.Faker('email')
    password= factory.PostGenerationMethodCall('set_password', 'default_password')

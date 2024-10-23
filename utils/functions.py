
from django.db.models import Func, IntegerField

class Position(Func):
    function = 'POSITION'
    template = '%(function)s(%(expression)s IN %(field)s)'
    output_field = IntegerField()
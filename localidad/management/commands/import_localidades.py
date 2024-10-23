import csv
from django.core.management import BaseCommand
from provincia.models import Provincia
from departamento.models import Departamento
from gobierno_local.models import GobiernoLocal
from localidad.models import Localidad


class Command(BaseCommand):
    help = 'Importar gobiernos locales a la base'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                provinciaID= Provincia.objects.get(nombre=row[7])
                departamentoID= Departamento.objects.get(nombre= row[6], provincia= provinciaID)
                gobiernoLocalID= GobiernoLocal.objects.get(nombre= row[5], departamento= departamentoID)
                Localidad.objects.create(
                    nombre = row[0],
                    codigo_UTA = row[1],
                    gobierno_local= gobiernoLocalID,
                    departamento = departamentoID,
                    provincia = provinciaID,

                )

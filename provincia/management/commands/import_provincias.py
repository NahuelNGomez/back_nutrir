import csv
from django.core.management import BaseCommand
from provincia.models import Provincia


class Command(BaseCommand):
    help = 'Importar provincias a la base'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row[4] == '':
                    row[4] = 0.0

                Provincia.objects.create(
                    # Identificacion
                    nombre=row[0],
                    codigo_UTA=row[7],
                )

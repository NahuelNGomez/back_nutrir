import csv
from django.core.management import BaseCommand
from provincia.models import Provincia
from departamento.models import Departamento


class Command(BaseCommand):
    help = 'Importar departamentos a la base'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                #import pdb
                #pdb.set_trace()
                if row[6] == '':
                    row[6] = 0.0
                if row[7] == '':
                    row[7] = 0.0
                if row[8] == '':
                    row[8] = 0.0
                provinciaID= Provincia.objects.get(nombre=row[5])

                Departamento.objects.create(
                    #Identificacion
                    nombre = row[0],
                    codigo_UTA=row[1],
                    provincia= provinciaID,

                )

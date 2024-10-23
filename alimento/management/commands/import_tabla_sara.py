import csv
from decimal import Decimal
from django.core.management import BaseCommand
from alimento.models import AlimentoSARA

class Command(BaseCommand):
    help = 'Importar datos de la tabla SARA'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Ruta del archivo CSV')

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        with open(path, 'rt', encoding='ISO-8859-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                AlimentoSARA.objects.update_or_create(
                    nombre = row['Alimento'][:100],  # maximo 100 caracteres
                    defaults = {
                        'cantidad_porcion': 1, # ACLARACION: Pongo 1 pero no se a que se refiere. No aparece en la tabla
                        'hidratos_carbono': Decimal(row.get('Hidratos de Carbono (g)', '0').replace(',', '.')),
                        'proteinas': Decimal(row.get('Proteínas (g)', '0').replace(',', '.')),
                        'grasas': Decimal(row.get('Ácidos Grasos Saturados (g)', '0').replace(',', '.')),
                        'grasas_totales': Decimal(row.get('Lípidos (g)', '0').replace(',', '.')),
                        'energia': Decimal(row.get('Energía (kcal)', '0').replace(',', '.')),
                        'sodio': Decimal(row.get('Sodio (mg)', '0').replace(',', '.')),
                    }

                )
                self.stdout.write(self.style.SUCCESS(f'Alimento {row["Alimento"]} importado con éxito.'))

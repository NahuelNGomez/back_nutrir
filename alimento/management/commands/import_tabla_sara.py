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

        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                # Función para convertir valores, manejando 'x' y valores vacíos
                def safe_decimal(value, default='0'):
                    if not value or value.strip() == '' or value.strip().lower() == 'x':
                        return Decimal(default)
                    return Decimal(str(value).replace(',', '.'))

                AlimentoSARA.objects.update_or_create(
                    nombre = row['Alimento'][:100],  # maximo 100 caracteres
                    defaults = {
                        'cantidad_porcion': Decimal('1'),
                        'hidratos_carbono': safe_decimal(row.get('Carbohidratos disponibles (g)', '0')),
                        'proteinas': safe_decimal(row.get('Proteínas (g)', '0')),
                        'grasas': safe_decimal(row.get('Saturados (g)', '0')),
                        'grasas_totales': safe_decimal(row.get('Lípidos totales (g)', '0')),
                        'energia': safe_decimal(row.get('Valor energético (Kcal)', '0')),
                        'sodio': safe_decimal(row.get('Sodio (mg)', '0')),
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Alimento {row["Alimento"]} importado con éxito.'))

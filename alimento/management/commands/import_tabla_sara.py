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
                        
                        # Nutrientes básicos
                        'agua': Decimal(row.get('Agua (g)', '0').replace(',', '.')),
                        'energia': Decimal(row.get('Energía (kcal)', '0').replace(',', '.')),
                        'proteinas': Decimal(row.get('Proteínas (g)', '0').replace(',', '.')),
                        'lipidos': Decimal(row.get('Lípidos (g)', '0').replace(',', '.')),
                        
                        # Ácidos grasos
                        'acidos_grasos_saturados': Decimal(row.get('Ácidos Grasos Saturados (g)', '0').replace(',', '.')),
                        'acidos_grasos_monoinsaturados': Decimal(row.get('Ácidos Grasos Monoinsaturados (g)', '0').replace(',', '.')),
                        'acidos_grasos_poliinsaturados': Decimal(row.get('Ácidos Grasos Poliinsaturados (g)', '0').replace(',', '.')),
                        'colesterol': Decimal(row.get('Colesterol (mg)', '0').replace(',', '.')),
                        
                        # Carbohidratos y fibra
                        'hidratos_carbono': Decimal(row.get('Hidratos de Carbono (g)', '0').replace(',', '.')),
                        'fibra': Decimal(row.get('Fibra (g)', '0').replace(',', '.')),
                        'cenizas': Decimal(row.get('Cenizas (g)', '0').replace(',', '.')),
                        
                        # Minerales
                        'sodio': Decimal(row.get('Sodio (mg)', '0').replace(',', '.')),
                        'potasio': Decimal(row.get('Potasio (mg)', '0').replace(',', '.')),
                        'calcio': Decimal(row.get('Calcio (mg)', '0').replace(',', '.')),
                        'fosforo': Decimal(row.get('Fósforo (mg)', '0').replace(',', '.')),
                        'hierro': Decimal(row.get('Hierro (mg)', '0').replace(',', '.')),
                        'zinc': Decimal(row.get('Zinc (mg)', '0').replace(',', '.')),
                        
                        # Vitaminas
                        'niacina': Decimal(row.get('Niacina (mg)', '0').replace(',', '.')),
                        'folatos': Decimal(row.get('Folatos (μg)', '0').replace(',', '.')),
                        'vitamina_a': Decimal(row.get('Vitamina A (μg RAE)', '0').replace(',', '.')),
                        'tiamina': Decimal(row.get('Tiamina (B1) (mg)', '0').replace(',', '.')),
                        'riboflavina': Decimal(row.get('Riboflavina (B2) (mg)', '0').replace(',', '.')),
                        'vitamina_b12': Decimal(row.get('Vitamina B12 (μg)', '0').replace(',', '.')),
                        'vitamina_c': Decimal(row.get('Vitamina C (mg)', '0').replace(',', '.')),
                        'vitamina_d': Decimal(row.get('Vitamina D (UI)', '0').replace(',', '.')),
                        
                        # Campos legacy para compatibilidad
                        'grasas': Decimal(row.get('Ácidos Grasos Saturados (g)', '0').replace(',', '.')),
                        'grasas_totales': Decimal(row.get('Lípidos (g)', '0').replace(',', '.')),
                    }

                )
                self.stdout.write(self.style.SUCCESS(f'Alimento {row["Alimento"]} importado con éxito.'))

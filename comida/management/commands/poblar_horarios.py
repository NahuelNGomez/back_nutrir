from django.core.management.base import BaseCommand
from comida.models import Horario

class Command(BaseCommand):
    help = 'Pobla la base de datos con los horarios iniciales'

    def handle(self, *args, **options):
        horarios_data = [
            ("desayuno_merienda_bebidas", "Desayuno/Merienda - Bebidas"),
            ("desayuno_merienda_comida", "Desayuno/Merienda - Comida"),
            ("almuerzo_cena_entrada", "Almuerzo/Cena - Entrada"),
            ("almuerzo_cena_plato_principal", "Almuerzo/Cena - Plato Principal"),
            ("almuerzo_cena_postre", "Almuerzo/Cena - Postre"),
        ]

        for codigo, nombre in horarios_data:
            horario, created = Horario.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Creado horario: {nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Horario ya existe: {nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS('Proceso completado')
        )

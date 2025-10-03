from django.core.management.base import BaseCommand
from admin_interface.models import Theme


class Command(BaseCommand):
    help = 'Configura el tema personalizado para la administración de Nutrir'

    def handle(self, *args, **options):
        # Obtener o crear el tema por defecto
        theme, created = Theme.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Nutrir Admin Theme',
                'title': 'Administración de Nutrir',
                'title_visible': True,
                'logo_visible': False,
                'title_color': '#FFFFFF',
                'logo_color': '#FFFFFF',
            }
        )
        
        if not created:
            # Actualizar el tema existente
            theme.name = 'Nutrir Admin Theme'
            theme.title = 'Administración de Nutrir'
            theme.title_visible = True
            theme.logo_visible = False
            theme.title_color = '#FFFFFF'
            theme.logo_color = '#FFFFFF'
            theme.save()
            
        self.stdout.write(
            self.style.SUCCESS(
                'Tema de administración configurado correctamente para Nutrir'
            )
        )

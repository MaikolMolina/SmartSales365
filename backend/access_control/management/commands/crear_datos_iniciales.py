from django.core.management.base import BaseCommand
from backend.access_control.models import Permiso, Rol, Usuario

class Command(BaseCommand):
    help = 'Crea datos iniciales para el sistema'

    def handle(self, *args, **options):
        # Crear permisos básicos
        permisos_data = [
            {'nombre': 'Gestionar Usuarios', 'codigo': 'user_manage'},
            {'nombre': 'Gestionar Roles', 'codigo': 'role_manage'},
            {'nombre': 'Gestionar Permisos', 'codigo': 'permission_manage'},
            {'nombre': 'Ver Bitácora', 'codigo': 'audit_view'},
        ]
        
        for perm_data in permisos_data:
            Permiso.objects.get_or_create(**perm_data)
        
        # Crear rol de administrador
        admin_rol, created = Rol.objects.get_or_create(
            nombre='Administrador',
            descripcion='Rol con todos los permisos del sistema'
        )
        
        if created:
            admin_rol.permisos.set(Permiso.objects.all())
        
        # Crear usuario administrador
        if not Usuario.objects.filter(username='admin').exists():
            admin_user = Usuario.objects.create_user(
                username='admin',
                email='admin@smartsales365.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                rol=admin_rol
            )
            self.stdout.write(
                self.style.SUCCESS('Usuario administrador creado: admin/admin123')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Datos iniciales creados exitosamente')
        )
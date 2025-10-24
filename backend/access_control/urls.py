from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importar directamente desde cada módulo
from .views.auth_views import login_view, logout_view
from .views.user_views import UsuarioViewSet
from .views.role_views import RolViewSet
from .views.permission_views import PermisoViewSet
from .views.audit_views import BitacoraViewSet


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'permisos', PermisoViewSet, basename='permiso')
router.register(r'bitacora', BitacoraViewSet, basename='bitacora')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

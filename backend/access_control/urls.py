from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importar directamente desde cada módulo
from .views import (
    auth_views, 
    user_views, 
    role_views, 
    permission_views, 
    audit_views
)
from .views import fcm_views


router = DefaultRouter()
router.register(r'usuarios', user_views.UsuarioViewSet, basename='usuario')
router.register(r'roles', role_views.RolViewSet, basename='rol')
router.register(r'permisos', permission_views.PermisoViewSet, basename='permiso')
router.register(r'bitacora', audit_views.BitacoraViewSet, basename='bitacora')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_client, name='register'), 
    path('save_fcm_token/', fcm_views.save_fcm_token, name='save_fcm_token'),
    path('remove_fcm_token/', fcm_views.remove_fcm_token, name='remove_fcm_token'),
]

from rest_framework import routers
from django.urls import path, include
from .views import (
    PacienteViewSet,
    HistorialClinicoViewSet,
    ContactoEmergenciaViewSet,
    UsuarioViewSet,
    RolViewSet,
    AntecedenteViewSet,
    AntecedenteConsolidadoViewSet,
)

router = routers.DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'historiales', HistorialClinicoViewSet)
router.register(r'contactos', ContactoEmergenciaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'roles', RolViewSet)
# Ruta para tabla padre de antecedentes
router.register(r'antecedentes', AntecedenteViewSet, basename='antecedentes')
# Ruta simple de antecedentes consolidados
router.register(r'antecedentes_consolidados', AntecedenteConsolidadoViewSet, basename='antecedentes_consolidados')

urlpatterns = [
    path('', include(router.urls)),
]
